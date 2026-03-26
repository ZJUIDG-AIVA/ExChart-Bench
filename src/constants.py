CSV_INST = \
"""You are a data analyst who needs to extract precise data from a chart and fill the blank cells in a CSV template.

OUTPUT FORMAT:
- Delimiter: comma (,).
- Produce exactly one code block tagged as csv and nothing else (no text before or after).
- Output complete CSV with header, which has {} rows x {} columns
- Copy the header and every non-blank cell exactly as they appear.
- Fill only the blank cells.
- Do not add, remove, reorder, or rename any rows or columns.

VALUE FORMATTING:
- If the chart's tick labels (not the axis title) use units such as "K", "M", "%", or "million", etc., output values with plain digits followed by the same units. For example:
	- If tick labels use "K", write values like 12.3K.
	- If tick labels use "M", write values like 4.2M.
	- If tick labels use "%", write values like 7.5%. If the chart is a pie chart, include the "%" sign as well.
	- If tick labels use "million", write values like 3.6 million.
	- If tick labels show plain digits (no unit), write the values as plain digits with no unit.
- Do not convert units or invent abbreviations. For example, if the tick labels do not show “K”, output plain digits 12300 instead of 12.3K.
- Do not use thousand separators or blank spaces in numbers.
- Keep as many significant digits as possible to maintain maximum precision.

TEMPLATE:
Place your completed CSV inside a single code block like:
```csv
<header row>
<other rows>
```

Here is the CSV with blank cells:
{}
"""