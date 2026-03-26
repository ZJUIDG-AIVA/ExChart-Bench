model_name=Qwen2.5-VL-7B-Instruct
model_path=Qwen/Qwen2.5-VL-7B-Instruct

python src/generate.py \
    --model_name $model_name \
    --data_dir dataset/ \
    --model_path $model_path