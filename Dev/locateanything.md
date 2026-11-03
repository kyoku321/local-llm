# 1. 克隆 Eagle 仓库并进入 Embodied 目录
git clone https://github.com/NVlabs/Eagle.git
cd Eagle/Embodied

# 2. 安装除 flash-attn 之外模型所需的依赖包（如 timm, einops 等）
pip install -e .



python batch_infer.py \
  --model /models/LocateAnything-3B \
  --attn la_flash \
  --vision-attn flash_attention_2 \
  --scheduler pipeline \
  --batch-size 4 \
  --image /workspace/conbini.jpg \
  --query "GABAミルク" \
  --out gaba_results.jsonl



python batch_infer_vis.py \
    --model /models/LocateAnything-3B \
    --attn la_flash \
    --vision-attn flash_attention_2 \
    --scheduler pipeline \
    --batch-size 4 \
    --image /workspace/conbini.jpg \
    --query "GABAミルク" \
    --outdir vis_output \
    --vis \
    --out gaba_results.jsonl


test-pod:/models/LocateAnything-3B/vis_output/conbini_vis.jpg
