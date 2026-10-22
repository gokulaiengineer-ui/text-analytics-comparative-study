"""Builds report/Term_Project_Report.pdf from results.json + figures/ (run after the notebook)."""
import json, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether)

R = json.load(open('results.json', encoding='utf-8'))
os.makedirs('report', exist_ok=True)
OUT = 'report/Term_Project_Report.pdf'
ss = getSampleStyleSheet()
B = ParagraphStyle('B', parent=ss['BodyText'], fontName='Times-Roman', fontSize=11.5, leading=17, alignment=TA_JUSTIFY, spaceAfter=7)
H1 = ParagraphStyle('H1', parent=ss['Heading1'], fontName='Times-Bold', fontSize=16, spaceBefore=12, spaceAfter=8)
H2 = ParagraphStyle('H2', parent=ss['Heading2'], fontName='Times-Bold', fontSize=13, spaceBefore=8, spaceAfter=5)
CAP = ParagraphStyle('CAP', parent=B, fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=colors.HexColor('#444444'))
CELL = ParagraphStyle('CELL', parent=B, fontName='Helvetica', fontSize=8.5, leading=10.5, alignment=0, spaceAfter=0)
CELLB = ParagraphStyle('CELLB', parent=CELL, fontName='Helvetica-Bold')
CT = ParagraphStyle('CT', parent=B, fontSize=22, leading=28, alignment=TA_CENTER, fontName='Times-Bold')
CS = ParagraphStyle('CS', parent=B, fontSize=13, leading=19, alignment=TA_CENTER)

def clean(s):
    return str(s).replace('✔', 'Yes').replace('✘', 'No').replace('◐', 'Partial').replace('≈', '~')
def table(rows, widths, head=True, font=CELL):
    data = [[Paragraph(clean(c), CELLB if (head and i == 0) else font) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#999999')), ('VALIGN', (0,0), (-1,-1), 'TOP'),
          ('LEFTPADDING', (0,0), (-1,-1), 4), ('RIGHTPADDING', (0,0), (-1,-1), 4)]
    if head: st.append(('BACKGROUND', (0,0), (-1,0), colors.HexColor('#DCE6F1')))
    t.setStyle(TableStyle(st)); return t
def fig(path, w, caption):
    img = Image(path); r = w / img.imageWidth; img.drawWidth = w; img.drawHeight = img.imageHeight * r
    return KeepTogether([img, Paragraph(caption, CAP), Spacer(1, 8)])
def P(t): return Paragraph(t, B)

M, SP, D, S = R['meta'], R['speed'], R['data'], R['speed']
have_cn = 'CoreNLP' in SP
ratio = SP['NLTK']['+ Lemma + NER']['docs_per_sec']
sp_full = SP['spaCy']['+ Lemma + NER']['docs_per_sec']; sp_pipe = SP['spaCy (nlp.pipe)']['+ Lemma + NER']['docs_per_sec']
x_full = sp_full / ratio; x_pipe = sp_pipe / ratio
acc = R['pos_accuracy']; st = R['startup']

s = []
s += [Spacer(1, 3*cm), Paragraph('TERM PROJECT REPORT', CS), Spacer(1, 1*cm),
      Paragraph('A Comparative Study of Open-Source Text Analytics Libraries', CT),
      Paragraph('NLTK, spaCy and Stanford CoreNLP', CS),
      Paragraph('Features, Ease of Use and Performance', CS), Spacer(1, 2*cm),
      Paragraph('Subject: Text Analytics', CS), Spacer(1, 0.6*cm),
      Paragraph('Submitted by', CS), Paragraph('<b>Santhana Krishnan S</b>', CS),
      Paragraph('Register No.: ______________________', CS), Spacer(1, 0.6*cm),
      Paragraph('Master of Computer Applications (2025 - 2027)', CS),
      Paragraph('Ayya Nadar Janaki Ammal College (Autonomous), Sivakasi', CS), Spacer(1, 0.6*cm),
      Paragraph('Under the guidance of: ______________________', CS),
      Paragraph(f'Date: {M["date"]}', CS), PageBreak()]

s += [Paragraph('Abstract', H1),
 P('Text analytics converts unstructured text into structured information, and most projects start by choosing a software library. '
   'This report compares three widely used open-source toolkits, NLTK, spaCy and Stanford CoreNLP, on three dimensions: the features they provide, how easy they are to use, and how they perform. '
   f'The same tasks (tokenization, part-of-speech tagging, lemmatization and named-entity recognition) were run on the same {D["n_docs"]} movie reviews ({D["total_chars"]:,} characters), and POS accuracy was measured on {D["pos_sentences"]} Penn Treebank sentences. '
   f'On our test machine NLTK was fastest for tokenization and POS-only processing, but when lemmatization and NER were added spaCy was about {x_full:.0f} times faster than NLTK ({x_pipe:.0f} times with batching). '
   f'POS accuracy was {acc["NLTK"]}% for NLTK and {acc["spaCy"]}% for spaCy. '
   'CoreNLP offers the deepest analysis (constituency parsing, coreference, OpenIE) at the cost of a Java server and a GPL licence. '
   'We conclude that NLTK suits learning, spaCy suits building applications, and CoreNLP suits tasks needing deep linguistic analysis.'),
 P('<b>Keywords:</b> text analytics, NLP, NLTK, spaCy, Stanford CoreNLP, benchmark.')]

s += [Paragraph('1. Introduction', H1),
 P('Natural Language Processing (NLP) libraries provide ready-made components such as tokenizers, taggers and parsers. Choosing among them affects development time, accuracy, speed and deployment cost. '
   'NLTK (Natural Language Toolkit) was created for teaching and research and bundles many corpora and algorithms. spaCy is an industrial-strength Python/Cython library designed for fast, production use. '
   'Stanford CoreNLP, written in Java, provides a broad suite of linguistic annotators developed by the Stanford NLP Group.'),
 Paragraph('1.1 Objectives', H2),
 P('(i) Compare the features of NLTK, spaCy and Stanford CoreNLP. (ii) Compare their ease of use in installation, code size and documentation. '
   '(iii) Compare their performance in speed, POS-tagging accuracy, start-up time and memory. (iv) Recommend the right library for typical use cases.'),
 Paragraph('1.2 Scope', H2),
 P('The study covers English text and four core tasks: tokenization with sentence splitting, POS tagging, lemmatization and named-entity recognition. '
   'Machine-learning model training and non-English languages are outside the scope.')]

s += [Paragraph('2. Overview of the Libraries', H1),
 table([['', 'NLTK', 'spaCy', 'Stanford CoreNLP'],
        ['Origin', 'University of Pennsylvania (2001)', 'Explosion AI (2015)', 'Stanford NLP Group'],
        ['Language', 'Python', 'Python / Cython', 'Java'],
        ['Licence', 'Apache 2.0', 'MIT', 'GPL v3 (commercial licence available)'],
        ['Philosophy', 'Teaching and research toolkit', 'Fast, production-ready pipelines', 'Deep linguistic analysis'],
        ['Version used', M['nltk'], f'{M["spacy"]} (model {M["spacy_model"]})', '4.5.x (see notebook)']],
       [3*cm, 4.3*cm, 4.3*cm, 4.4*cm]), Spacer(1, 6)]

s += [Paragraph('3. Methodology', H1),
 P(f'<b>Environment.</b> Python {M["python"]}, {M["cpu_count"]} CPU core, {M["platform"]}. All code is in the accompanying Jupyter Notebook.'),
 P(f'<b>Data.</b> Speed was measured on {D["n_docs"]} movie reviews from the NLTK <i>movie_reviews</i> corpus (average {D["avg_chars"]:,} characters). '
   f'Accuracy was measured on the first {D["pos_sentences"]} sentences ({D["pos_tokens"]:,} tokens) of the NLTK Penn Treebank sample, with traces removed. All three libraries use the Penn Treebank tag set, so tags are directly comparable; pre-tokenized input was supplied so token boundaries match the gold data.'),
 P('<b>Pipelines timed.</b> (a) tokenization with sentence splitting; (b) tokenization + POS tagging; (c) tokenization + POS + lemmatization + NER. '
   'Each document was processed in its own call; one warm-up call was made; the median of repeated runs is reported (3 runs for (a) and (b), 2 for (c) with NLTK). '
   'For spaCy, the dependency parser was disabled in (c) to match the other libraries; a batched run using <i>nlp.pipe</i> is also reported.'),
 P('<b>Start-up and memory.</b> Each library was loaded in a fresh process and the increase in resident memory and the time to load and run one sentence were recorded.')]

s += [Paragraph('4. Feature Comparison', H1),
 P('Table 1 summarizes what each library provides out of the box. "Partial" means the capability exists only in limited form or needs an add-on.'),
 table([['Feature', 'NLTK', 'spaCy', 'CoreNLP']] + [r for r in R['features']], [4.2*cm, 4.1*cm, 3.8*cm, 4.1*cm]),
 Paragraph('Table 1: Feature comparison (compiled from official documentation).', CAP), Spacer(1, 6),
 P('NLTK is unique in shipping corpora and lexicons (WordNet, Brown, Treebank, VADER) and stemmers. spaCy supplies a coherent, pretrained pipeline including a dependency parser and 18 entity types, plus word vectors in larger models. '
   'CoreNLP is the only one of the three with built-in constituency parsing, coreference resolution and OpenIE.')]

s += [Paragraph('5. Ease of Use', H1),
 table([['Aspect', 'NLTK', 'spaCy', 'CoreNLP']] + [r for r in R['ease']['table']], [3.6*cm, 4.3*cm, 4.3*cm, 4.0*cm]),
 Paragraph('Table 2: Ease-of-use comparison.', CAP), Spacer(1, 6),
 P(f'For the same job (tokens, POS tags, lemmas, entities for one text) NLTK needed {R["ease"]["loc"]["NLTK"]} lines, spaCy {R["ease"]["loc"]["spaCy"]} lines and CoreNLP {R["ease"]["loc"]["CoreNLP"]} lines. '
   'NLTK needs several separate data downloads and a manual POS-tag conversion before WordNet lemmatization. spaCy returns rich Doc/Token objects, so everything comes from one call. '
   'CoreNLP requires Java, a large download and a running server, and returns JSON that must be unpacked, although this also makes it usable from any language.'),
 KeepTogether([Paragraph('Author\'s rating (1 = poor, 5 = excellent)', H2),
 table([['Criterion', 'NLTK', 'spaCy', 'CoreNLP']] + [[r[0], r[1], r[2], r[3]] for r in R['scores']], [6*cm, 3.4*cm, 3.4*cm, 3.4*cm]),
 Paragraph('Table 3: Qualitative scores (subjective, based on Sections 4 and 5).', CAP)])]

s += [PageBreak(), Paragraph('6. Performance Results', H1), Paragraph('6.1 Speed', H2)]
rows = [['Library', 'Task', 'Docs/sec', 'Tokens/sec', 'Total sec']]
for lib, d in SP.items():
    for task, v in d.items(): rows.append([lib, task, v['docs_per_sec'], f'{v["tokens_per_sec"]:,}', v['seconds']])
if not have_cn:
    rows.append(['Stanford CoreNLP', 'all', 'not measured', 'not measured', '-'])
s += [table(rows, [3.6*cm, 3.6*cm, 3*cm, 3.3*cm, 2.7*cm]), Paragraph(f'Table 4: Processing speed on {D["n_docs"]} reviews.', CAP), Spacer(1, 6)]
if not have_cn:
    s += [P('<b>Note on CoreNLP.</b> The environment used to generate this version of the report had no access to the Stanford download site, so CoreNLP could not be run and no CoreNLP numbers are reported. '
            'Running the notebook on Google Colab or a machine with Java adds the CoreNLP rows automatically; re-run <i>build_report.py</i> to include them.')]
s += [fig('figures/speed.png', 13*cm, 'Figure 1: Documents processed per second (log scale).'),
 P(f'Tokenization and POS-only processing were fast in both libraries, with NLTK ahead on this machine ({SP["NLTK"]["+ POS tagging"]["docs_per_sec"]} vs {SP["spaCy"]["+ POS tagging"]["docs_per_sec"]} documents/s for POS). '
   f'The picture reverses once NER is included: NLTK\'s <i>ne_chunk</i> is expensive, so NLTK fell to {ratio} documents/s while spaCy reached {sp_full} ({sp_pipe} with <i>nlp.pipe</i>), a speed-up of about {x_full:.0f} times ({x_pipe:.0f} times batched). '
   'spaCy also produces richer, neural-model-based entity labels in that time.'),
 KeepTogether([Paragraph('6.2 POS-tagging accuracy', H2),
 fig('figures/pos_accuracy.png', 9.5*cm, 'Figure 2: POS accuracy on 500 Penn Treebank sentences.')]),
 P(f'NLTK scored {acc["NLTK"]}% and spaCy {acc["spaCy"]}%. The gap is small, and the Treebank sample overlaps with the training data of some taggers, so the figures are optimistic and should be read only as a relative comparison. '
   'The small spaCy model trades a little accuracy for speed and size.'),
 KeepTogether([Paragraph('6.3 Start-up time and memory', H2),
 fig('figures/startup_memory.png', 12.5*cm, 'Figure 3: Time to load and extra memory used.')]),
 P(f'NLTK took {st["NLTK"]["startup_sec"]} s and {st["NLTK"]["memory_mb"]} MB to load the tagger, chunker and WordNet, while spaCy took {st["spaCy"]["startup_sec"]} s and {st["spaCy"]["memory_mb"]} MB. '
   + ('CoreNLP: %s s start-up and %s MB. ' % (st['CoreNLP']['startup_sec'], st['CoreNLP']['memory_mb']) if 'CoreNLP' in st else
      'CoreNLP runs in a separate JVM and typically needs a few gigabytes of heap for the full annotator set, but this was not measured here.'))]

s += [Paragraph('7. Discussion', H1),
 P('<b>Features.</b> CoreNLP is broadest in linguistic depth, spaCy gives the most complete ready-to-use pipeline in Python, and NLTK gives the most educational material and classical tools such as stemmers and lexicons. '
   '<b>Ease of use.</b> spaCy needed the fewest steps and lines; NLTK is simple per function but needs more glue code and data downloads; CoreNLP has the highest set-up cost. '
   '<b>Performance.</b> Results depend on the task. Speed in simple tasks does not predict speed in a full pipeline, so benchmarks must use the pipeline that the application actually needs. '
   '<b>Licensing and deployment.</b> NLTK (Apache 2.0) and spaCy (MIT) are easy to use commercially; CoreNLP is GPL v3 and needs a commercial licence for closed-source products.'),
 Paragraph('Recommendations', H2),
 table([['Use case', 'Suggested library'],
        ['Learning NLP concepts, classroom work, corpora and lexicons', 'NLTK'],
        ['Production pipelines, information extraction, web services', 'spaCy'],
        ['Coreference, constituency parsing, OpenIE, temporal expressions', 'Stanford CoreNLP'],
        ['Quick stemming or VADER sentiment baseline', 'NLTK']], [11*cm, 4.5*cm])]

s += [Paragraph('8. Conclusion', H1),
 P('Each library has a clear role. NLTK is the best learning toolkit, spaCy offers the best balance of speed, simplicity and accuracy for applications, and CoreNLP provides the deepest analysis when those extra annotators are required. '
   'The measurements showed that the faster library depends on the task: NLTK was ahead for tokenization and POS only, while spaCy was far faster once NER and lemmatization were included.'),
 Paragraph('Limitations and future work', H2),
 P('The study used 100 documents, one machine, English text and the small spaCy model. The Treebank sample overlaps with training data of some taggers. CoreNLP timings include HTTP and JSON overhead. '
   'Future work: add the transformer-based spaCy model and Stanza, evaluate NER against a labelled dataset such as CoNLL-2003, and test larger corpora and multiple languages.')]

s += [Paragraph('References', H1)]
refs = ['Bird, S., Klein, E., and Loper, E. (2009). Natural Language Processing with Python. O\'Reilly Media.',
 'Honnibal, M., Montani, I., Van Landeghem, S., and Boyd, A. (2020). spaCy: Industrial-strength Natural Language Processing in Python. Zenodo.',
 'Manning, C. D., Surdeanu, M., Bauer, J., Finkel, J., Bethard, S. J., and McClosky, D. (2014). The Stanford CoreNLP Natural Language Processing Toolkit. Proceedings of ACL: System Demonstrations, pp. 55-60.',
 'Marcus, M. P., Santorini, B., and Marcinkiewicz, M. A. (1993). Building a large annotated corpus of English: the Penn Treebank. Computational Linguistics, 19(2).',
 'NLTK documentation: https://www.nltk.org',
 'spaCy documentation: https://spacy.io',
 'Stanford CoreNLP documentation: https://stanfordnlp.github.io/CoreNLP/']
for i, r in enumerate(refs, 1): s.append(P(f'[{i}] {r}'))

def foot(c, d):
    c.saveState(); c.setFont('Helvetica', 8); c.drawCentredString(A4[0]/2, 1.2*cm, f'Text Analytics Term Project  -  Page {d.page}'); c.restoreState()
SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2.5*cm, rightMargin=2.5*cm, topMargin=2.3*cm, bottomMargin=2.2*cm,
                  title='Comparative Study of NLTK, spaCy and Stanford CoreNLP', author='Santhana Krishnan S').build(s, onFirstPage=lambda c, d: None, onLaterPages=foot)
print('Wrote', OUT)
