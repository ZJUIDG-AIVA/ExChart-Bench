# ExChart-Bench

## 📄 Introduction
This repository provides the code and data for **ExChart-Bench**, introduced in our CHI 2026 paper: *"Making Multimodal LLMs Reliable Chart Data Extractors: A Benchmark and Training Framework."*

<a href=https://exchart.github.io><img src='https://img.shields.io/badge/Project_Page-Website-green?logo=googlechrome&logoColor=white' alt='Project Page'></a>

## 🆕 Update
- **Mar 2026**: We manually debugged the dataset, fixing several annotation errors and image issues, and improving the accuracy of manually extracted values.
- **Mar 2026**: Initial release of ExChart-Bench code and dataset.

## 🔨 Quick Start
1. Setup the environment
```bash
conda create -n exchart python=3.10 -y
conda activate exchart
pip install -r requirements.txt
```
2. Download the dataset from [Google Drive](https://drive.google.com/file/d/11_BteeRrY-tDRA2_cSB6zOXW-BUHrAyA/view?usp=drive_link), and place the `dataset` folder in the root directory of this repository.

## 💻 Prompting VLMs to Extract Data from Charts

`generate.sh` provides an example of prompting Qwen2.5-VL-Instruct to extract data from charts.

```bash
bash generate.sh
```

### Output

Results are saved in the results/ directory as JSON files with the following structure:
```json
{
  "00000.png": {
      "figure_id": "00000.png",
      "response": "```csv\n\"class\",\"Romania\",\"Togo\",\"Zambia\"\n\"1995\",63000,146000,218000\n\"2001\",47000,89000,286000\n\"2004\",5000,70000,141000\n\"2005\",5000,70000,48000\n```"
  },
  ...
}
```

## 🧮 Get Evaluation Results

`evaluate.sh` provides an example of evaluating the generated results of Qwen2.5-VL-Instruct on the ExChart-Bench dataset.

```bash
bash evaluate.sh
```

## Citation
If you find our work useful for your research please cite:
```
@inproceedings{he2026exchart,
  author = {He, Yuchen and Ying, Peizhi and Cheng, Liqi and Peng, Kuilin and Tian, Yuan and Deng, Dazhen and Wu, Yingcai},
  title = {Making Multimodal LLMs Reliable Chart Data Extractors: A Benchmark and Training Framework},
  year = {2026},
  isbn = {9798400722783},
  publisher = {Association for Computing Machinery},
  address = {New York, NY, USA},
  url = {https://doi.org/10.1145/3772318.3790721},
  doi = {10.1145/3772318.3790721},
  booktitle = {Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems},
  series = {CHI '26}
}
```