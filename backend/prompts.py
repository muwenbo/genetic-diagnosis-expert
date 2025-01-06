
TEST_TEMPLATE = """Hello AI, You will be provided with a research article and a genetic variant to analyze. The article is:
<RESEARCH_ARTICLE>
{pubmed_article}
</RESEARCH_ARTICLE>

The genetic variant to analyze is:
<GENETIC_VARIANT>
{genetic_variant}
</GENETIC_VARIANT>"""

GENE_EXPLAINATION_TEMPLATE = """作为遗传学专家，你的职责是阅读基因相关的英文信息，并总结归纳成基因疾病相关性的描述。请遵循以下准则：

1. 以基因名称为主语进行描述，需求强调基因的致病变异会导致相关疾病，并说明遗传模式。
2. 如果基因信息中包含疾病的患者信息，需要简要总结疾病的患者可能存在的临床表现。
3. 疾病名称需要为中文名（英文名）[MIM:omim id]的格式。
4. 不分行，以一个段落进行输出；字数不超过500字。

<<表型关系/phenotype map>>: {phenotype}
<<基因信息/molecular genetics>>:{molecular_genetics}"""

PUBMED_ACMG_READER_TEMPLATE = """You are an AI agent tasked with classifying inherited genetic variants based on the American College of Medical Genetics and Genomics (ACMG) guidelines.
You are tasked with analyzing a scientific article to determine if certain conditions exist regarding a specific genetic variant. 
Follow these steps carefully:

1. You will be provided with a research article and a genetic variant to analyze. The article is:
<RESEARCH_ARTICLE>
{pubmed_article}
</RESEARCH_ARTICLE>

The genetic variant to analyze is:
<GENETIC_VARIANT>
{genetic_variant}
</GENETIC_VARIANT>

2. Read the full text of the article associated with the provided PubMed ID. Pay close attention to any information related to the specified genetic variant.

3. Analyze the article to determine if any of the following conditions exist regarding the genetic variant:

a) De novo occurrence:
   - De novo (both maternity and paternity confirmed) in a patient with the disease and no family history.
   - Assumed de novo, but without confirmation of paternity and maternity.

b) Functional studies:
   - Well-established in vitro or in vivo functional studies supportive of a damaging effect on the gene or gene product.
   - Well-established in vitro or in vivo functional studies show no damaging effect on protein function or splicing.

c) Prevalence and observation:
   - The prevalence of the variant in affected individuals is significantly increased compared with the prevalence in controls.
   - The same variant observed in multiple unrelated affected individuals with consistent phenotypes, and its absence in population databases.

d) Cosegregation:
   - Cosegregation with disease in multiple affected family members in a gene definitively known to cause the disease.
   - Lack of segregation in affected members of a family.

e) Phenotype specificity:
   - Patient's phenotype or family history is highly specific for a disease with a single genetic etiology.

f) Trans or cis occurrence:
   - Observed in trans with a pathogenic variant for a fully penetrant dominant gene/disorder.
   - Observed in cis with a pathogenic variant in any inheritance pattern.

g) Alternative molecular basis:
   - Variant found in a case with an alternate molecular basis for disease.

4. For each condition, provide a brief explanation of your findings. If the information is not available or not applicable, state so clearly.

5. Present your analysis in the following markdown format:

### Analysis
**de_novo_occurrence**:
[Your findings for de novo occurrence]

**functional_studies**:
[Your findings for functional studies]

**prevalence_and_observation**:
[Your findings for prevalence and observation]

**cosegregation**:
[Your findings for cosegregation]

**phenotype_specificity**:
[Your findings for phenotype specificity]

**trans_cis_occurrence**:
[Your findings for trans or cis occurrence]

**alternative_molecular_basis**:
[Your findings for alternative molecular basis]

6. After presenting your analysis, provide a brief summary of the most significant findings regarding the genetic variant in relation to the conditions analyzed in Chinese. Present this summary below a H3 header "Summary".

7. If the full article is not available, give a note at the beginning of your reply.

Remember to base your analysis solely on the information provided in the article associated with the given PubMed ID. Do not make assumptions or include information from external sources.
"""

ACMG_CLASSIFIER_TEMPLATE = """You are an AI agent tasked with analyzing genetic variant annotations and providing ACMG classification insights.

The variant to analyze is:
<VARIANT>
{genetic_variant}
</VARIANT>

The variant annotation data is:
<ANNOTATION>
{annotation}
</ANNOTATION>

Please analyze the annotation data and provide:

1. A summary of the variant's key characteristics including:
   - Gene and transcript information
   - Variant type and location
   - Predicted functional impact
   - Population frequencies
   - Clinical significance from databases

2. Relevant ACMG criteria that can be applied based on the annotation data:
   - PP3/BP4: In silico predictions (SIFT, PolyPhen)
   - PM2: Population frequency
   - PP5/BP6: Reputable source classification
   
3. A preliminary classification suggestion based on available evidence.

Present your analysis in markdown format with appropriate headers and bullet points.
"""

ACMG_CLASSIFIER_COMPLETE_TEMPLATE = """
You are an AI agent tasked with classifying inherited genetic variants based on the American College of Medical Genetics and Genomics (ACMG) guidelines. Your goal is to analyze the provided variant information and determine its pathogenicity classification.

First, familiarize yourself with the ACMG guidelines for variant classification:

<ACMG_GUIDELINES>
| Category | Code | Description/Criteria |
|----------|------|-------------------|
| Very Strong | PVS1 | Null variant (nonsense, frameshift, canonical ±1/2 splice sites, initiation codon, single/multiexon deletions) in gene where LOF is known disease mechanism |
| Strong | PS1 | Same amino acid change as previously established pathogenic variant regardless of nucleotide change |
| | PS2 | De novo (both maternity and paternity confirmed) in patient with disease and no family history |
| | PS3 | Well-established functional studies show damaging effect |
| | PS4 | Variant prevalence in affected individuals significantly increased vs controls |
| Moderate | PM1 | Located in mutational hot spot and/or critical functional domain |
| | PM2 | Absent from controls or at extremely low frequency if recessive |
| | PM3 | For recessive disorders, detected in trans with pathogenic variant |
| | PM4 | Protein length changes due to in-frame deletions/insertions or stop-loss variants |
| | PM5 | Novel missense change at amino acid where different missense change is known to be pathogenic |
| | PM6 | Assumed de novo, but without confirmation of paternity and maternity |
| Supporting | PP1 | Cosegregation with disease in multiple affected family members |
| | PP2 | Missense variant in gene with low rate of benign missense variation |
| | PP3 | Multiple lines of computational evidence support deleterious effect |
| | PP4 | Patient's phenotype/family history specific for disease with single genetic etiology |
| | PP5 | Reputable source reports variant as pathogenic |

Important Caveats and Notes:
1. Beware of genes where LOF is not a known disease mechanism
2. Use caution with splice variants at extreme 3' end of gene
3. For statistical information (PS4), relative risk should be >5.0
4. Population data for insertions/deletions may be poorly called by next-generation sequencing
5. Multiple computational algorithms should not be counted as independent criteria
6. Functional studies should be validated and reproducible in clinical diagnostic laboratory settings

| Category | Code | Description/Criteria |
|----------|------|-------------------|
| Stand-alone | BA1 | Allele frequency is >5% in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium |
| Strong | BS1 | Allele frequency is greater than expected for disorder |
| | BS2 | Observed in healthy adult for recessive (homozygous), dominant (heterozygous), or X-linked (hemizygous) disorder with full penetrance expected at early age |
| | BS3 | Well-established functional studies show no damaging effect on protein function or splicing |
| | BS4 | Lack of segregation in affected members of a family |
| Supporting | BP1 | Missense variant in gene for which primarily truncating variants cause disease |
| | BP2 | Observed in trans with pathogenic variant for fully penetrant dominant gene/disorder or observed cis with a pathogenic variant in any inheritance pattern |
| | BP3 | In-frame insertions/deletions in repetitive region without known function |
| | BP4 | Multiple lines of computational evidence suggest no impact on gene or product |
| | BP5 | Variant found in case with alternate molecular basis for disease |
| | BP6 | Reputable source reports variant as benign |
| | BP7 | A synonymous/silent variant for which splicing prediction algorithms predict no impact |

Important Caveats:
1. For common phenotypes (e.g., cancer, epilepsy), lack of segregation among affected individuals should be interpreted with caution
2. Families may have more than one pathogenic variant contributing to autosomal dominant disease
3. For computational evidence (BP4), because many algorithms use similar input, each algorithm cannot be counted independently
4. Evidence from reputable sources should be available to the laboratory to perform independent evaluation
</ACMG_GUIDELINES>

Now, you will be presented with information about a genetic variant in json format to classify:

The variant to analyze is:
<VARIANT>
{genetic_variant}
</VARIANT>

The variant annotation data is:
<ANNOTATION>
{annotation}
</ANNOTATION>

To classify the variant, follow these steps:

1. Carefully analyze the variant information against each ACMG criterion.
1.1 Follow the decision trees for PVS1 criteria.
<PVS1_decision_tree>
Nonsense or Frameshift:
If predicted to undergo NMD (Nonsense-Mediated Decay):
If exon is present in biologically-relevant transcripts → PVS1
If exon is absent from biologically-relevant transcripts → N/A
If not predicted to undergo NMD:
If truncated/altered region is critical to protein function → PVS1_Strong
For LoF variants in this exon:
If frequent in general population/exon absent → N/A
If not frequent and:
Variant removes >10% of protein → PVS1_Strong
Variant removes <10% of protein → PVS1_Moderate
GT-AG ±2 splice sites:
If exon skipping/cryptic splice site disrupts reading frame and predicted for NMD:
If exon present in relevant transcripts → PVS1
If exon absent from relevant transcripts → N/A
If not predicted for NMD:
If region critical to function → PVS1_Strong
For LoF variants: Similar criteria as nonsense/frameshift
If preserves reading frame:
Similar decision tree based on LoF variant frequency and protein impact
Initiation Codon:
No known alternative start codon:
≥1 pathogenic variant(s) upstream → PVS1_Moderate
No pathogenic variant(s) upstream → PVS1_Supp
Different functional transcript uses alternative start codon → N/A
</PVS1_decision_tree>

1.2 Do not use criteria PP5 and BP6.
1.3 Do not use any information from ClinVar.
2. Use a scratchpad to document your thought process and evidence for each criterion.
3. Determine which criteria are met and their strength (very strong, strong, moderate, or supporting).
4. Based on the combination of criteria met, determine the final classification (pathogenic, likely pathogenic, variant of uncertain significance, likely benign, or benign).
5. Provide a justification for your classification.
6. Write the variant HGVS at the beginning of your output.

Begin your analysis by using a scratchpad to evaluate each ACMG criterion:

**scratchpad**
[Evaluate each ACMG criterion here, noting which are met and their strength]


After completing your analysis, provide your final classification and justification within the following tags:

**classification**
[State the final classification here: pathogenic, likely pathogenic, variant of uncertain significance, likely benign, or benign]

**justification**
[Provide a detailed justification for your classification, referencing the specific ACMG criteria that were met and how they contributed to your decision]

Remember to be thorough in your analysis and clear in your explanation. If there is insufficient information to classify the variant confidently, state this in your justification and classify it as a variant of uncertain significance.
"""

PVS1_EXPERT_TEMPLATE = """You are tasked with performing a comprehensive ACMG PVS1 rule assessment based on the PVS1 decision tree. You will be provided with variant annotation, gene annotation, and transcript annotation data. Your goal is to analyze this information and determine the appropriate PVS1 classification.

First, review the provided information:

<variant_annotation>
{variant_annotation}
</variant_annotation>

<gene_annotation>
{gene_annotation}
</gene_annotation>

<transcript_annotation>
{transcript_annotation}
</transcript_annotation>

Now, follow these steps to perform the PVS1 assessment:

1. Determine the variant type based on the variant annotation. Is it a nonsense variant, frameshift variant, or affecting GT-AG intronic splice sites?

2. Based on the variant type, follow the appropriate branch of the decision tree:

   For Nonsense or Frameshift Variants:
   a. Determine if the variant is predicted to undergo NMD.
   b. Check if the affected exon is present in biologically-relevant transcripts.
   c. If not undergoing NMD, assess the role of the region in protein function and the frequency of LoF variants in the general population.
   d. Calculate the percentage of protein removed by the variant.

   For GT-AG Intronic Splice Sites:
   a. Predict if exon skipping or use of a cryptic splice site will occur.
   b. Determine if the resulting change disrupts the reading frame.
   c. Assess if the variant is predicted to undergo NMD.
   d. If not undergoing NMD, follow similar steps as for nonsense/frameshift variants.

3. Use the gene and transcript annotations to support your analysis, particularly when assessing biologically-relevant transcripts and the importance of affected regions.

4. Based on your analysis, determine the appropriate PVS1 classification: PVS1, PVS1_Strong, PVS1_Moderate, or Not met.

5. Provide your reasoning and final assessment in the following format:

**reasoning**
Explain your step-by-step analysis here, referencing the relevant parts of the decision tree and the provided annotations. Include any assumptions or uncertainties in your assessment.

**pvs1_assessment**
State the final PVS1 classification here (PVS1, PVS1_Strong, PVS1_Moderate, or Not met).

Remember to consider all aspects of the decision tree and use the provided annotations to support your assessment. If there is insufficient information to make a definitive classification, state this clearly in your reasoning and provide the most appropriate classification based on the available data.
"""