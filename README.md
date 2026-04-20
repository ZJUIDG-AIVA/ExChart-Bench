# 📈👉🔢 ExChart-Bench

> **Making Multimodal LLMs Reliable Chart Data Extractors: A Benchmark and Training Framework**  
> Yuchen He, Peizhi Ying, Liqi Cheng, Kuilin Peng, Dazhen Deng, Yingcai Wu  
> Published at CHI 2026 | [Paper](https://dl.acm.org/doi/pdf/10.1145/3772318.3790721) | [Website](https://exchart.github.io/)

<a href=https://exchart.github.io><img src='https://img.shields.io/badge/Project_Page-Website-green?logo=googlechrome&logoColor=white' alt='Project Page'></a>

## Abstract

Chart data extraction, which reverse-engineers data tables from chart images, is essential for reproducibility, analysis, retrieval, and redesign. Existing interactive tools are reliable but tedious, and mixed-initiative systems, while more efficient, lack generalizability. Recent multimodal large language models (MLLMs) offer a unified interface for chart interpretation, yet their ability to extract accurate data tables, especially without visible labels, remains unclear. We build a benchmark featuring diverse real-world charts without data labels to evaluate this capability. Results show that, while current MLLMs reliably reconstruct table structures, they struggle with precise value recovery. To address this, we revisit chart data extraction from a human-centered perspective and argue that extraction should follow a progressive learning process similar to how people read charts. Our training framework substantially improves numerical accuracy, achieving state-of-the-art performance with a 7B-parameter model. A user study further shows that our model effectively supports mixed-initiative workflows for reliable chart data extraction.

## 🔥 News
- [2026-03] We manually debugged the dataset, fixing several annotation errors and image issues, and improving the accuracy of manually extracted values.
- [2026-03] Release of ExChart-Bench code and dataset.
- [2026-02] ExChart-Bench accepted at CHI 2026!

## Getting Started

### Installation
```bash
conda create -n exchart python=3.10 -y
conda activate exchart
pip install -r requirements.txt
```

### Data Preparation
Download the dataset from [Google Drive](https://drive.google.com/file/d/11_BteeRrY-tDRA2_cSB6zOXW-BUHrAyA/view?usp=drive_link), and place the `dataset` folder in the root directory of this repository.

### Prompting VLMs to Extract Data from Charts

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

### Get Evaluation Results

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

## License
This project is licensed under [GNU GPL v3](LICENSE).
