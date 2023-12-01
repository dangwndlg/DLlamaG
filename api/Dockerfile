FROM ubuntu:latest

RUN apt update
RUN apt install python3 python3-pip -y
RUN mkdir -p /mnt/api
WORKDIR /mnt/api

ARG LLAMA_CKPT_DIR="/root/llama/llama-2-7b-chat"
ARG LLAMA_TOKENIZER_PATH="/root/llama/tokenizer.model"

ENV BUILD_LLAMA="true"
ENV ENABLE_LOGGING="true"
ENV LLAMA_CKPT_DIR=${LLAMA_CKPT_DIR}
ENV LLAMA_TOKENIZER_PATH=${LLAMA_TOKENIZER_PATH}

COPY ${LLAMA_CKPT_DIR} ${LLAMA_CKPT_DIR}
COPY ${LLAMA_TOKENIZER_PATH} ${LLAMA_TOKENIZER_PATH}

# Copy code
COPY . .

RUN pip install -r ./requirements.txt

# CMD [ "torchrun", "--nproc_per_node", "1", "src/main.py" ]