# Problem statement

## Terminal Illness Diagnosis  kidney Disease
Nephrologists are finding increase in chronic kidney disease(CKD),kidney infections, kidney stones, kidney cancer and end–stage kidney disease(ESKD) .
By Leveraging AI accurate diagnoses, optimize treatment plans, identify high risk and low risk patients, enhance patient monitoring and deliver enhanced value.

## The Different Stages of Chronic Kidney Disease
Chronic kidney disease is a progressive condition that involves the gradual loss of kidney function over time. 
Based on the results of the eGFR (estimated glomerular filtration rate) test that measures the patient’s kidney function and filtration rate, 
the patient falls into one of below mentioned 1 – 5 stages of CKD: 

![image](https://github.com/user-attachments/assets/811b67e8-7ba4-4100-bb2c-5e7e7990978d)


# Solution architecture
Below is a high level solution diagram, which proposes a mult-agent solution to automate the CKD detection workflow.

![image](https://github.com/user-attachments/assets/14d7b49c-955f-4886-b832-a0f363405e04)

# Solution - proof of concept
The current proof of concept (PoC) solution is implemented using CrewAI based agentic AI framework. 
It targets the Agent1 functionality shown in the solution architecture diagram above.

It implements 2 agents:
* First agent takes a person's blood report as a input PDF (image flattened PDF meaning it has blood report as a scanned image not text) and uses the open source document processing project called docling, implemented as a tool for the agent, to convert the PDF into a JSON using the OCR (optical character recognition) functionality of the docling tool.
* Second agent takes the JSON as a input and extracts the field of interest, using custom python code, implemented as a tool for the agent.

## PoC demo video
Here is a small video that demonstrates the code in action...

https://github.com/user-attachments/assets/234ab2f5-2c55-4f09-baed-ff30c11b4615
