# Comparative Study of NLTK, spaCy and Stanford CoreNLP

Text Analytics term project - Santhana Krishnan S, MCA, Ayya Nadar Janaki Ammal College, Sivakasi.

Compares three open-source text analytics libraries on **features, ease of use and performance**
(tokenization, POS tagging, lemmatization, NER) using the same 100 movie reviews and 500 Penn Treebank sentences.

## Files
| File | Purpose |
|---|---|
| `text_analytics_comparison.ipynb` | Complete Jupyter Notebook (executed, with outputs) |
| `report/Term_Project_Report.pdf` | Term project report |
| `report/Output_Screenshots.pdf` | Notebook outputs as PDF |
| `results.json`, `figures/` | Measured results and charts |
| `build_report.py` | Rebuilds the report PDF from `results.json` |
| `demo_video_script.md` | Script for the MP4 demo |

## Run
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
jupyter notebook text_analytics_comparison.ipynb
```
Stanford CoreNLP needs Java (JDK 8+). The notebook downloads CoreNLP (~500 MB) and starts its server automatically.
Easiest: upload the notebook to **Google Colab** (Java is preinstalled), run all cells, download `results.json` and `figures/`,
then run `python build_report.py` to regenerate the report with CoreNLP numbers.

## Results (NLTK / spaCy; CoreNLP is measured when the notebook is run with Java)
See the report, Section 6.
