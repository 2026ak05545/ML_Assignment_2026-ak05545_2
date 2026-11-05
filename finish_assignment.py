from pathlib import Path
import csv,sys,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PIL
root=Path(__file__).parent
out=root/'BITS_ML_Assignment_2_Finalization_Report.pdf'
metrics=root/'model_comparison_results.csv'
linkfile=root/'streamlit_link.txt'
streamlit=linkfile.read_text().strip() if linkfile.exists() else ''
rows=[]
if metrics.exists():
 with metrics.open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='H0x',fontName='Helvetica-Bold',fontSize=15,leading=19,alignment=TA_CENTER,spaceAfter=9))
styles.add(ParagraphStyle(name='H1x',fontName='Helvetica-Bold',fontSize=11,leading=14,spaceBefore=12,spaceAfter=6))
styles.add(ParagraphStyle(name='Px',fontName='Helvetica',fontSize=9,leading=13,spaceAfter=7))
styles.add(ParagraphStyle(name='Sx',fontName='Helvetica',fontSize=7.5,leading=10,spaceAfter=5))
doc=SimpleDocTemplate(str(out),pagesize=(595,842),leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=45)
story=[]
def p(s,style='Px'):story.append(Paragraph(s,styles[style]))
def h(s):p(s,'H1x')
def esc(s):return html.escape(str(s))
p('M.Tech (Artificial Intelligence and Machine Learning)','H0x');p('Machine Learning - Assignment 2','H0x');p('Adult Income Classification: Comparison of Five Models')
p('<b>Completion status:</b> '+('Metrics loaded from supplied CSV. ' if rows else 'Measured model scores are pending. ')+('Streamlit URL supplied.' if streamlit else 'Working Streamlit URL pending.')+' Verify all links and the deployed application before submission.')
h('1. GitHub repository link')
p('<link href="https://github.com/2026ak05545/ML_Assignment_2026-ak05545_2" color="black"><u>https://github.com/2026ak05545/ML_Assignment_2026-ak05545_2</u></link>')
p('The repository is intended to hold the notebook, application code, requirements, README, labelled test CSV and five saved preprocessing-and-classifier pipelines. Verify the latest committed files in the main branch.')
h('2. Live Streamlit application link')
p(('<link href="'+esc(streamlit)+'" color="black"><u>'+esc(streamlit)+'</u></link>') if streamlit else '<b>Pending:</b> Paste the verified application URL into streamlit_link.txt and rerun finish_assignment.py.')
p('The application must load trained pipelines without retraining, accept a labelled CSV and show model selection, six scores, and a confusion matrix or classification report.')
h('3. Evidence of BITS Virtual Lab execution')
p('The following screenshot shows work performed inside the BITS Prayogshala environment. A screenshot showing the completed notebook execution is preferable if available.')
img=root/'BITS_lab_grayscale.png'
if img.exists():story.append(Image(str(img),width=500,height=265))
p('Figure 1. Work in the BITS Virtual Lab environment (grayscale).','Sx')
h('4. README content')
h('a. Problem statement')
p('This project examines whether a person earns more than USD 50,000 annually using demographic and employment information. I compare five classification algorithms using a common training and testing procedure. My aim is to understand not only which model makes the most correct predictions, but also which one identifies higher-income records reliably.')
h('b. Dataset description')
p('The UCI Adult (Census Income) dataset provides 14 input features and the target column income, with classes &lt;=50K and &gt;50K. The original UCI adult.data file contains 32,561 records. The notebook removes missing and duplicate records, selects a reproducible stratified subset of at most 12,000 records, and uses an 80:20 stratified split with random seed 42. Final working counts must be confirmed from the notebook output.')
p('Source: https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data','Sx')
h('c. GitHub repository')
p('https://github.com/2026ak05545/ML_Assignment_2026-ak05545_2')
h('d. Classification models and measured comparison')
p('The five methods are Logistic Regression, Decision Tree, K-Nearest Neighbors, Gaussian Naive Bayes, and Support Vector Machine. The saved pipelines combine preprocessing with the fitted classifier. Numerical and categorical columns are processed consistently across the models.')
name_order=['Logistic Regression','Decision Tree','K-Nearest Neighbors','Gaussian Naive Bayes','Support Vector Machine']
byname={r.get('ML Model Name','').lower().strip():r for r in rows}
short=['Logistic Regression','Decision Tree','KNN','Naive Bayes','SVM']
values=[['Model','Accuracy','AUC','Precision','Recall','F1','MCC']]
for name,label in zip(name_order,short):
 r=byname.get(name.lower(),{})
 def val(k):
  try:return f'{float(r[k]):.4f}'
  except:return 'Pending'
 values.append([label]+[val(k) for k in ['Accuracy','AUC','Precision','Recall','F1 Score','MCC']])
t=Table(values,colWidths=[112,65,52,69,59,56,55],repeatRows=1,hAlign='LEFT')
t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.black),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(1,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story.append(t)
h('Observations for each model')
notes={'Logistic Regression':'This is the linear reference model. Its test F1 and MCC indicate how well a straightforward decision boundary works.', 'Decision Tree':'This model uses interpretable splits. Its test scores help assess whether those rules generalize to unseen examples.', 'K-Nearest Neighbors':'This model classifies records using similar training examples. Recall and F1 are especially useful for assessing its higher-income predictions.', 'Gaussian Naive Bayes':'This probabilistic model is computationally simple, but its feature assumptions may limit performance.', 'Support Vector Machine':'This model seeks a separating boundary. Its F1, AUC and MCC show how well it handles the two income groups.'}
for name in name_order:
 r=byname.get(name.lower())
 detail=(' On the measured test data, accuracy was '+f'{float(r["Accuracy"]):.4f}'+' and F1 was '+f'{float(r["F1 Score"]):.4f}'+'.') if r and r.get('Accuracy') and r.get('F1 Score') else ' Actual performance must be described after the test run.'
 p('<b>'+name+':</b> '+notes[name]+detail)
if rows:
 try:
  winner=max(rows,key=lambda r:float(r['F1 Score']))
  p('<b>Overall winning model (highest test F1):</b> '+esc(winner['ML Model Name'])+'. This ranking should be interpreted alongside MCC, AUC and the application outputs.')
 except:p('<b>Overall winner:</b> Pending validation of metric values.')
else:p('<b>Overall winner:</b> Pending actual model comparison results. The notebook ranks models by test F1.')
h('Evaluation and application workflow')
p('Accuracy describes the proportion of correct predictions. AUC measures ranking across classification thresholds. Precision measures the correctness of positive predictions, recall measures detection of positive examples, F1 balances precision and recall, and MCC summarizes performance across all confusion-matrix cells. The Streamlit interface calculates these measures on the uploaded labelled test data without fitting models again.')
h('Final checks before submitting')
p('Confirm that five trained .joblib pipelines and test_data.csv are committed to GitHub; that Streamlit loads without errors; that its dropdown, metrics and confusion matrix work; and that the screenshot shows BITS Virtual Lab execution. The final portal upload must be one PDF, not the project ZIP.')
if not rows or not streamlit:p('<b>NOT READY FOR FINAL SUBMISSION:</b> This PDF contains unresolved items. Do not upload it as the final assignment until these are filled and verified.')
def foot(c,d):c.setStrokeColor(colors.black);c.line(44,33,551,33);c.setFont('Helvetica',8);c.drawString(44,22,'Machine Learning - Assignment 2');c.drawRightString(551,22,f'Page {d.page}')
doc.build(story,onFirstPage=foot,onLaterPages=foot)
print(out)
