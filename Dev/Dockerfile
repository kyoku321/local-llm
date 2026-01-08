# 从轻量级的 Python 镜像开始
FROM python:3.12-slim

# 使用 Debian 12 (bookworm) 的软件包源，这是 python:3.12-slim (基于Debian 12) 推荐的
# 注意：我们将 CUDA_VERSION 更改为 12.1，以便更容易匹配 PyTorch 版本的依赖
ENV CUDA_VERSION="12-1"
ENV DEBIAN_FRONTEND=noninteractive

# 2. 安装必要的构建工具和 CUDA 运行时库
RUN apt update \
    # 步骤 1: 安装必要的工具
    && apt install -y curl gnupg wget \
    # 步骤 2: 下载并安装 NVIDIA CUDA 仓库配置 Deb 包
    # 这个包会自动导入密钥，并创建正确的 /etc/apt/sources.list.d/cuda.list 文件
    && wget https://developer.download.nvidia.com/compute/cuda/repos/debian12/x86_64/cuda-keyring_1.1-1_all.deb \
    && dpkg -i cuda-keyring_1.1-1_all.deb \
    # 步骤 3: 重新更新 apt 列表，以便识别新的 NVIDIA 包
    && apt update \
    # 步骤 4: **核心步骤:** 安装 CUDA 运行时库
    # 我们只安装轻量的运行时库 `cuda-runtime`，它会拉取必要的 `cuda-libraries` 等
    # 安装 libcudnn$CUDA_VERSION 时，注意版本号格式可能需要调整，这里我们安装 cuda-toolkit-12-1 提供的 runtime
    && apt install -y \
        cuda-runtime-$CUDA_VERSION \
        libcublas-$CUDA_VERSION \
        # 注意：libcudnn的版本号格式是 libcudnn8，需要额外处理，这里我们先使用官方的运行时包
    && rm -f cuda-keyring_1.1-1_all.deb \
    # 清理：删除下载的包列表和安装文件以减小镜像体积
    && rm -rf /var/lib/apt/lists/*
    
# 3. 安装 PyTorch/TensorFlow 等 Python 库 (例如 PyTorch 2.1)
# 注意：你需要安装与你所选 CUDA 版本匹配的 Python 库
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

# 定义容器启动时的默认命令
CMD ["python3"]