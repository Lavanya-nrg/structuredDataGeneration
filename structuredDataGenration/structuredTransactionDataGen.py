import json
import os
from typing import Optional
from dotenv import load_dotenv
from langchain.chains.openai_functions import create_structured_output_chain
from langchain_openai import ChatOpenAI 
from langchain.prompts import ChatPromptTemplate

load_dotenv() 
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
json_schema={
    "title": "Transaction",
    "description": "Information about a transaction.",
    "type": "object",
    "properties": {
        "transaction_id": {"title": "Transaction ID", "type": "string"},
        "date": {"title": "Date", "type": "string", "format": "date"},
        "total_amount": {"title": "Total Amount", "type": "number"},
        "customer_id": {"title": "Customer ID", "type": "string"},
        "first_name": {"title": "First Name", "type": "string"},
        "last_name": {"title": "Last Name", "type": "string"},
        "email": {"title": "Email", "type": "string", "pattern": "^\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"},
        "ssn": {"title": "SSN", "type": "string", "pattern": "^\\d{3}-\\d{2}-\\d{4}$"},
        "orders": {
            "title": "Orders",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "order_id": {"title": "Order ID", "type": "string"},
                    "order_date": {"title": "Order Date", "type": "string", "format": "date"},
                    "subtotal": {"title": "Subtotal", "type": "number"},
                    "products": {
                        "title": "Products",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"title": "Product ID", "type": "string"},
                                "product_name": {"title": "Product Name", "type": "string"},
                                "quantity": {"title": "Quantity", "type": "integer"},
                                "price": {"title": "Price", "type": "number"}
                            },
                            "required": ["product_id", "product_name", "quantity", "price"]
                        }
                    }
                },
                "required": ["order_id", "order_date", "subtotal", "products"]
            }
        }
    },
    "required": ["transaction_id", "date", "total_amount", "customer_id", "first_name", "last_name", "email", "ssn", "orders"]
}



transactions_json_schema = {
    "title": "Transactions",
    "description": "A list of transactions.",
    "type": "object",
    "properties": {
        "transactions": {
            "title": "Transactions",
            "description": "A list of transactions",
            "type": "array",
            "items": json_schema
        }
    }
}


llm = ChatOpenAI(model="gpt-4", temperature=0)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are extracting information in structured formats."),
        ("human", "Use the given format to generate {number} random data with {type} transaction id ranging between TRX021 to TRX040 and cust id between CUST021 to CUST040.Names of customers should be different from the previous 20 transactions.")
    ]
)

chain = create_structured_output_chain(transactions_json_schema, llm, prompt, verbose=True)
output = chain.run({
    "number": 20,
    "type": "TRX"
})
with open('output2.json', 'w') as f:
    json.dump(output, f)

print(output)

# import json
# import os
# from dotenv import load_dotenv
# from langchain.chains.openai_functions import create_structured_output_chain
# from langchain_openai import ChatOpenAI 
# from langchain.prompts import ChatPromptTemplate

# load_dotenv() 
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # Define JSON schema
# json_schema = {
#     "title": "Transaction",
#     "description": "Information about a transaction.",
#     "type": "object",
#     "properties": {
#         "transaction_id": {"title": "Transaction ID", "type": "string"},
#         "date": {"title": "Date", "type": "string", "format": "date"},
#         "total_amount": {"title": "Total Amount", "type": "number"},
#         "customer_id": {"title": "Customer ID", "type": "string"},
#         "first_name": {"title": "First Name", "type": "string"},
#         "last_name": {"title": "Last Name", "type": "string"},
#         "email": {"title": "Email", "type": "string", "pattern": r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"},
#         "ssn": {"title": "SSN", "type": "string", "pattern": r"^\d{3}-\d{2}-\d{4}$"},
#         "orders": {
#             "title": "Orders",
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {"title": "Order ID", "type": "string"},
#                     "order_date": {"title": "Order Date", "type": "string", "format": "date"},
#                     "subtotal": {"title": "Subtotal", "type": "number"},
#                     "products": {
#                         "title": "Products",
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "product_id": {"title": "Product ID", "type": "string"},
#                                 "product_name": {"title": "Product Name", "type": "string"},
#                                 "quantity": {"title": "Quantity", "type": "integer"},
#                                 "price": {"title": "Price", "type": "number"}
#                             },
#                             "required": ["product_id", "product_name", "quantity", "price"]
#                         }
#                     }
#                 },
#                 "required": ["order_id", "order_date", "subtotal", "products"]
#             }
#         }
#     },
#     "required": ["transaction_id", "date", "total_amount", "customer_id", "first_name", "last_name", "email", "ssn", "orders"]
# }
# transactions_json_schema = {
#     "title": "Transactions",
#     "description": "A list of transactions.",
#     "type": "object",
#     "properties": {
#         "transactions": {
#             "title": "Transactions",
#             "description": "A list of transactions",
#             "type": "array",
#             "items": json_schema
#         }
#     }
# }

# # Define prompt
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are extracting information in structured formats."),
#         ("human", "Use the given format to generate 100 random data with TRX transaction id.")
#     ]
# )

# # Initialize OpenAI model
# llm = ChatOpenAI(model="gpt-4", temperature=0.5)

# # Create structured output chain
# chain = create_structured_output_chain(transactions_json_schema, llm, prompt, verbose=True)

# # Generate output (100 data)
# outputs = []
# for _ in range(100):
#     output = chain.run({})
#     outputs.append(output)

# # Write output to file
# with open('output.json', 'w') as f:
#     json.dump(outputs, f)

# print(outputs)


# import json
# import os
# from dotenv import load_dotenv
# from langchain.chains.openai_functions import create_structured_output_chain
# from langchain_openai import ChatOpenAI 
# from langchain.prompts import ChatPromptTemplate

# load_dotenv() 
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# # Define JSON schema
# json_schema = {
#     "title": "Transaction",
#     "description": "Information about a transaction.",
#     "type": "object",
#     "properties": {
#         "transaction_id": {"title": "Transaction ID", "type": "string"},
#         "date": {"title": "Date", "type": "string", "format": "date"},
#         "total_amount": {"title": "Total Amount", "type": "number"},
#         "customer_id": {"title": "Customer ID", "type": "string"},
#         "first_name": {"title": "First Name", "type": "string"},
#         "last_name": {"title": "Last Name", "type": "string"},
#         "email": {"title": "Email", "type": "string", "pattern": r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"},
#         "ssn": {"title": "SSN", "type": "string", "pattern": r"^\d{3}-\d{2}-\d{4}$"},
#         "orders": {
#             "title": "Orders",
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "properties": {
#                     "order_id": {"title": "Order ID", "type": "string"},
#                     "order_date": {"title": "Order Date", "type": "string", "format": "date"},
#                     "subtotal": {"title": "Subtotal", "type": "number"},
#                     "products": {
#                         "title": "Products",
#                         "type": "array",
#                         "items": {
#                             "type": "object",
#                             "properties": {
#                                 "product_id": {"title": "Product ID", "type": "string"},
#                                 "product_name": {"title": "Product Name", "type": "string"},
#                                 "quantity": {"title": "Quantity", "type": "integer"},
#                                 "price": {"title": "Price", "type": "number"}
#                             },
#                             "required": ["product_id", "product_name", "quantity", "price"]
#                         }
#                     }
#                 },
#                 "required": ["order_id", "order_date", "subtotal", "products"]
#             }
#         }
#     },
#     "required": ["transaction_id", "date", "total_amount", "customer_id", "first_name", "last_name", "email", "ssn", "orders"]
# }

# transactions_json_schema = {
#     "title": "Transactions",
#     "description": "A list of transactions.",
#     "type": "object",
#     "properties": {
#         "transactions": {
#             "title": "Transactions",
#             "description": "A list of transactions",
#             "type": "array",
#             "items": json_schema
#         }
#     }
# }

# # Define prompt
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are extracting information in structured formats."),
#         ("human", "Generate 100 JSON data entries with different values.")
#     ]
# )

# # Initialize OpenAI model
# llm = ChatOpenAI(model="gpt-4", temperature=0.5)

# # Create structured output chain
# chain = create_structured_output_chain(transactions_json_schema, llm, prompt, verbose=True)

# # Generate output (100 data)
# outputs = []
# for _ in range(100):
#     output = chain.run({})
#     outputs.append(output)

# # Write output to file
# with open('output.json', 'w') as f:
#     json.dump(outputs, f)

# print(outputs)
