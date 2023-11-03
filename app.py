import streamlit as st
from token_counter import num_tokens_from_string

st.title('Amazon Bedrock ESTIMATION Pricing Calculator')

tab1, tab2, tab3 = st.tabs(["Bedrock Pricing", "RAG Solution Data Store", "FAQs"])

with tab1:
    provider = st.selectbox('Select model provider', ['AI21 Labs', 'Amazon', 'Anthropic', 'Cohere', 'Stability AI'])

    if provider == 'AI21 Labs':

        st.header('AI21 Labs')
        st.write('Only On-Demand pricing is currently available')

        model = st.selectbox('Select model', ['Jurassic-2 Mid', 'Jurassic-2 Ultra'])

        input_tokens = st.number_input('Input tokens', min_value=0, max_value=1000000, value=1000)
        output_tokens = st.number_input('Output tokens', min_value=0, max_value=1000000, value=1000)
        customer_requests = st.number_input("Customer Requests per Day", min_value=0, max_value=1000000, value=500)

        if model == 'Jurassic-2 Mid':
            input_price = 0.0125
            output_price = 0.0125
        else:
            input_price = 0.0188
            output_price = 0.0188

        bedrock_cost = (((input_tokens / 1000) * input_price) + ((output_tokens / 1000) * output_price)) * customer_requests

        st.write(f'Total Bedrock Cost (Daily): ${bedrock_cost:.2f}')

    elif provider == 'Amazon':

        st.header('Amazon')

        pricing_option = st.radio('Select pricing option', ['On-Demand', 'Provisioned Throughput', 'Model Customization'])

        if pricing_option == 'On-Demand':
            model = st.selectbox('Select model', ['Titan Text - Lite', 'Titan Text - Express', 'Titan Embeddings'])

            input_tokens = st.number_input('Input tokens', min_value=0, max_value=1000000, value=1000)

            if model == 'Titan Text - Lite':
                input_price = 0.0003
                output_price = 0.0004
            elif model == 'Titan Text - Express':
                input_price = 0.0013
                output_price = 0.0017
            else:
                input_price = 0.0001
                output_price = 0

            if model != 'Titan Embeddings':
                output_tokens = st.number_input('Output tokens', min_value=0, max_value=1000000, value=1000)
                customer_requests = st.number_input("Customer Requests per Day", min_value=0, max_value=1000000, value=500)
                bedrock_cost = (((input_tokens / 1000) * input_price) + ((output_tokens / 1000) * output_price)) * customer_requests
            else:
                customer_requests = st.number_input("Customer Requests per Day", min_value=0, max_value=1000000,
                                                    value=500)
                bedrock_cost = ((input_tokens / 1000) * input_price) * customer_requests

            st.write(f'Total Bedrock Cost (Daily): ${bedrock_cost:.4f}')

        elif pricing_option == 'Provisioned Throughput':
            model = st.selectbox('Select model', ['Titan Text - Lite', 'Titan Text - Express', 'Titan Embeddings'])
            model_units = st.number_input('Number of model units', min_value=1, max_value=10, value=1)
            term = st.selectbox('Commitment term', ['1 month', '6 months'])

            if model == 'Titan Text - Lite':
                if term == '1 month':
                    price = 6.40
                else:
                    price = 5.10
            elif model == 'Titan Text - Express':
                if term == '1 month':
                    price = 18.40
                else:
                    price = 14.80
            else:
                if term == '1 month':
                    price = 6.40
                else:
                    price = 5.10

            bedrock_cost = model_units * price * 24 * 30

            st.write(f'Total monthly bedrock_cost: ${bedrock_cost:.2f}')

        else:
            model = st.selectbox('Select model', ['Titan Text - Lite', 'Titan Text - Express'])
            tokens = st.number_input('Number of tokens trained', min_value=0)
            epochs = st.number_input('Number of epochs', min_value=1, value=1)
            months = st.number_input('Number of months', min_value=1, value=1)

            if model == 'Titan Text - Lite':
                train_price = 0.0004
                store_price = 1.95
                infer_price = 7.10
            else:
                train_price = 0.0008
                store_price = 1.95
                infer_price = 20.50

            train_bedrock_cost = tokens * epochs * (train_price / 1000)
            store_bedrock_cost = store_price * months
            infer_bedrock_cost = infer_price * 1 * 24 * 30  # 1 model unit

            st.write(f'Training bedrock_cost: ${train_bedrock_cost:.2f}')
            st.write(f'Storage bedrock_cost: ${store_bedrock_cost:.2f}')
            st.write(f'Inference bedrock_cost: ${infer_bedrock_cost:.2f}')

    elif provider == 'Anthropic':

        st.header('Anthropic')

        pricing_option = st.radio('Select pricing option', ['On-Demand', 'Provisioned Throughput'])

        if pricing_option == 'On-Demand':
            model = st.selectbox('Select model', ['Claude', 'Claude Instant'])

            input_tokens = st.number_input('Input tokens', min_value=0, max_value=1000000, value=11000)
            output_tokens = st.number_input('Output tokens', min_value=0, max_value=1000000, value=4000)
            customer_requests = st.number_input("Customer Requests per Day", min_value=0, max_value=1000000, value=500)

            if model == 'Claude':
                input_price = 0.01102
                output_price = 0.03268
            else:
                input_price = 0.00163
                output_price = 0.00551

            bedrock_cost = (((input_tokens / 1000) * input_price) + ((output_tokens / 1000) * output_price)) * customer_requests

            st.write(f'Total Bedrock Cost (Daily): ${bedrock_cost:.2f}')

        else:
            model = st.selectbox('Select model', ['Claude Instant', 'Claude'])
            model_units = st.number_input('Number of model units', min_value=1, max_value=10, value=1)
            term = st.selectbox('Commitment term', ['1 month', '6 months'])

            if model == 'Claude Instant':
                if term == '1 month':
                    price = 39.60
                else:
                    price = 22.00
            else:
                if term == '1 month':
                    price = 63.00
                else:
                    price = 35.00

            bedrock_cost = model_units * price * 24 * 30

            st.write(f'Total monthly bedrock_cost: ${bedrock_cost:.2f}')

    elif provider == 'Cohere':

        st.header('Cohere')
        st.write('Only On-Demand pricing is currently available')

        model = st.selectbox('Select model', ['Command'])

        input_tokens = st.number_input('Input tokens', min_value=0, max_value=1000000, value=6000)
        output_tokens = st.number_input('Output tokens', min_value=0, max_value=1000000, value=2000)
        customer_requests = st.number_input("Customer Requests per Day", min_value=0, max_value=1000000, value=500)

        input_price = 0.0015
        output_price = 0.002

        bedrock_cost = (((input_tokens / 1000) * input_price) + ((output_tokens / 1000) * output_price)) * customer_requests

        st.write(f'Total Bedrock Cost (Daily): ${bedrock_cost:.3f}')

    else:

        st.header('Stability AI')

        pricing_option = st.radio('Select pricing option', ['On-Demand', 'Provisioned Throughput'])

        if pricing_option == 'On-Demand':

            model = st.selectbox('Select model', ['SDXL0.8', 'SDXL1.0'])

            image_resolution = st.selectbox('Image resolution', ['512x512 or smaller', 'Larger than 512x512'])
            image_quality = st.selectbox('Image quality', ['Standard (<51 steps)', 'Premium (>51 steps)'])

            images = st.number_input('Number of images', min_value=0, max_value=1000, value=1)
            customer_requests = st.number_input("Customer Requests per Day", min_value=0, max_value=1000000, value=500)

            if model == 'SDXL0.8':
                if image_resolution == '512x512 or smaller':
                    if image_quality == 'Standard (<51 steps)':
                        price = 0.018
                    else:
                        price = 0.036
                else:
                    if image_quality == 'Standard (<51 steps)':
                        price = 0.036
                    else:
                        price = 0.072
            else:
                if image_resolution == '512x512 or smaller':
                    if image_quality == 'Standard (<51 steps)':
                        price = 0.020
                    else:
                        price = 0.040
                else:
                    if image_quality == 'Standard (<51 steps)':
                        price = 0.040
                    else:
                        price = 0.080

            bedrock_cost = images * price * customer_requests

            st.write(f'Total Bedrock Cost (Daily): ${bedrock_cost:.3f}')

        else:
            model = st.selectbox('Select model', ['SDXL1.0'])
            model_units = st.number_input('Number of model units', min_value=1, max_value=10, value=1)
            term = st.selectbox('Commitment term', ['1 month', '6 months'])

            if term == '1 month':
                price = 49.86
            else:
                price = 46.18

            bedrock_cost = model_units * price * 24 * 30

            st.write(f'Total monthly bedrock_cost: ${bedrock_cost:.2f}')
with tab2:
    provider = st.selectbox('Select RAG Data Store', ['Amazon Kendra', 'Amazon OpenSearch Serverless Vector Store'])
    opensearch_cost = 0
    kendra_cost = 0
    if provider == 'Amazon Kendra':
        st.header('Amazon Kendra')

        kendra_edition = st.selectbox('Select Kendra Edition', ['Developer', 'Enterprise'])

        if kendra_edition == 'Developer':
            price_per_month = 810

            connector_usage = st.selectbox('Will you use a Kendra Connector?', ["Yes", "No"])
            if connector_usage == 'Yes':
                connector_docs_scanned = st.number_input("How many documents do you anticipate scanning?", min_value=1, max_value=100000, value=1)
                connector_usage_hours = st.number_input("How many hours do expect the Kendra sync to take, to be conservative estimate 1GB an hour to sync", min_value=1, max_value=10000, value=1)

                connector_docs_scanned_price = connector_docs_scanned * 0.000001
                connector_usage_hours_price = connector_usage_hours * 0.35
            else:
                connector_docs_scanned_price = 0
                connector_usage_hours_price = 0
            kendra_cost = price_per_month + connector_usage_hours_price + connector_docs_scanned_price
        elif kendra_edition == 'Enterprise':
            price_per_month = 1008
            connector_usage = st.selectbox('Will you use a Kendra Connector?', ["Yes", "No"])
            if connector_usage == 'Yes':
                connector_docs_scanned = st.number_input("How many documents do you anticipate scanning?", min_value=1, max_value=100000, value=1)
                connector_usage_hours = st.number_input("How many hours do expect the Kendra sync to take, to be conservative estimate 1GB an hour to sync", min_value=1, max_value=10000, value=1)

                connector_docs_scanned_price = connector_docs_scanned * 0.000001
                connector_usage_hours_price = connector_usage_hours * 0.35
            else:
                connector_docs_scanned_price = 0
                connector_usage_hours_price = 0

            storage_additional_capacity = st.number_input("How many documents do you expect to store in total?", min_value=0, max_value=10000000, value=0)
            query_additional_capacity = st.number_input("How many queries do you expect per day?", min_value=0, max_value=100000, value=0)
            if storage_additional_capacity > 100000:
                storage_additional_capacity_pricing = (storage_additional_capacity // 100000.0001) * (.7 * 24 * 30)
            else:
                storage_additional_capacity_pricing = 0

            if query_additional_capacity > 8000:
                query_additional_capacity_pricing = (query_additional_capacity // 8000.0001) * (.7 * 24 * 30)
            else:
                query_additional_capacity_pricing = 0
            kendra_cost = price_per_month + connector_usage_hours_price + connector_docs_scanned_price + storage_additional_capacity_pricing + query_additional_capacity_pricing
        st.write(f'Total monthly Kendra Cost: ${kendra_cost:.2f}')
    if provider == 'Amazon OpenSearch Serverless Vector Store':
        kendra_cost = 0

        indexing_OCU = st.number_input("How many OpenSearch Compute Units (OCU's) do you expect to consume for indexing (hourly)? (minimum of 2)", min_value=2, max_value=10000, value=2)
        search_and_query_OCU = st.number_input("How many OpenSearch Compute Units (OCU's) do you expect to consume for Search and Querying (hourly)? (minimum of 2)", min_value=2,max_value=10000, value=2)
        managed_storage = st.number_input("How many GB of data do you expect to store within OpenSearch Serverless Vector Search? (monthly)", min_value=0,max_value=10000, value=0)

        indexing_OCU_pricing = (indexing_OCU * 730) * 0.24
        search_and_query_OCU_pricing = (search_and_query_OCU * 730) * 0.24
        managed_storage_OCU_pricing = managed_storage * 0.24
        opensearch_cost = indexing_OCU_pricing + search_and_query_OCU_pricing + managed_storage_OCU_pricing
    st.write(f'Total monthly OpenSearch Serverless Vector Store Cost: ${opensearch_cost:.2f}')

with tab3:
    st.header("FREQUENTLY ASKED QUESTIONS:")
    with st.expander("What are input tokens?"):
        st.image("images/input_tokens.png")
        st.write(f"""
        Prompts: Prompts are the examples that you are passing into the model.
        
        Context: These are the results that are retrieved from your data store, such as Amazon Kendra or Amazon OpenSearch Vector Search.
        
        User Question: This is the user question that is being input and asked against the Amazon Bedrock.
        """)
    with st.expander("What are output tokens?"):
        st.image("images/output_tokens.png")
        st.write(f"""
        Total output tokens contain all the tokens generated by Amazon Bedrock (LLM).
        """)

with st.sidebar:
    st.header("TOTAL MONTHLY COST:")
    st.write(f'Total Bedrock Cost: ${bedrock_cost * 30:.2f}')
    st.write(f'Total Kendra Cost: ${kendra_cost:.2f}')
    st.write(f'Total OpenSearch Cost: ${opensearch_cost:.2f}')
    st.write(f'Total Solution Cost: ${((bedrock_cost * 30) + kendra_cost + opensearch_cost):.2f}')
    with st.expander("TOKEN COUNTER"):
        txt = st.text_area("Insert your text below to calculate how many tokens it is equivalent to:")
        button = st.button("Calculate Tokens")
        if button:
            st.header(f"""This piece of text contains {num_tokens_from_string(txt)} Tokens""")
