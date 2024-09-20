from pinecone import Pinecone, ServerlessSpec
pc = Pinecone(api_key="05315737-30f8-4042-9800-9208a0fa91d6")
index_name = "multilingual-e5-large"

class ChunkEmbed:
    def __init__(self):
        pass


    def chunker(self, document_text, max_chunk_size=90):
        # Calling chunk_text function to divide the text into chunks.
        words = document_text.split()
        chunks = []
        current_chunk = []

        for word in words:
            current_chunk.append(word)
            if len(current_chunk) >= max_chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []

        # Append any leftover words as the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        print(f"Number of chunks: {len(chunks)}")
        # print(chunks)  # First chunk

        chunked_data = []
        for i, chunk in enumerate(chunks):
            chunked_data.append({"id": str(i), "text": chunk})

        return chunked_data



    def create_pine_embeddings(self,data, document_name):

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1024,  # Replace with your model dimensions
                metric="cosine",  # Replace with your model metric
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )

            )
            # index = pc.Index('multilingual-e5-large')
        index = pc.Index('multilingual-e5-large')
        inputs = [item['text'] for item in data]  # Extract only the 'text' field

        embeddings = pc.inference.embed(
            model="multilingual-e5-large",
            inputs=inputs,
            parameters={"input_type": "passage"}
        )

        vectors = []
        for idx, (d, e) in enumerate(zip(data, embeddings)):
            unique_id = f"{document_name}_{d['id']}_{idx}"  # Create a unique ID using document name and chunk index
            vectors.append({
                "id": unique_id,
                "values": e['values'],
                "metadata": {'text': d['text'], 'document': document_name}
            })

        index.upsert(
            vectors=vectors,
            namespace="ns1"
        )






