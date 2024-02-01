# ssh into the arc server

# install NVIDIA tool kit
# https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation

# build ollama service
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# run llama2 model
docker exec -it ollama ollama run llama2