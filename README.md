# Geographic Bias Tool
Geographic Bias Tool aims to present data on the diversity of countries and country income level of authors. You can submit DOIs of publications to see the authors' country affiliations and country income statuses.
The tool aims to identify authors of given DOIs and found their country affiliations. Countries are ranked based on [World Bank GNI per capita, Atlas method](https://data.worldbank.org/indicator/NY.GNP.PCAP.CD). 
The [Citation Source Index](https://github.com/yusufaliozkan/geographic-bias-tool/tree/main?tab=readme-ov-file#what-is-citation-source-index-csi) is calculated to show the geographic bias of the given publication set.
# Who developed the Geographic Bias Tool?
The tool is developed by researchers and professional staff of [Imperial College London](https://www.imperial.ac.uk/admin-services/library/learning-support/geo-bias/).
# What is Citation Source Index (CSI)?
Citation Source Index (CSI) is a weighted average of the World Bank rankings for Gross National Income (GNI) per capita of the countries where the authors in that citation are from.

The CSI ranges from 0 to 1, so a CSI closer to 1 means the overall development index of the countries represented by the authors that published the article is high or vice versa. If the authors on an article were all from Afghanistan then the CSI would be 0.01. If the authors on an article were all from the UK then the CSI would be 0.88. The CSI for the reading list as a whole is the average of all the CSI scores for the readings provided on that list and that are available for analysis through this platform.

For more information, the following article: https://link.springer.com/article/10.1007/s11192-021-04231-3
# Where the data comes from?
Publications data (title, author name(s), country affiliations) are retrieved through [OpenAlex API](https://docs.openalex.org/how-to-use-the-api/api-overview).

Countries are ranked by using [World Bank GNI per capita, Atlas method](https://data.worldbank.org/indicator/NY.GNP.PCAP.CD).

Country income statuses are retrieved from [World Bank API](https://api.worldbank.org/v2/country/?per_page=1000).
# Reading list
Harris, Matthew. Decolonizing Healthcare Innovation: Low-Cost Solutions from Low-Income Countries. Routledge, 2024, https://www.routledge.com/Decolonizing-Healthcare-Innovation-Low-Cost-Solutions-from-Low-Income-Countries/Harris/p/book/9781032284958.

Harris, Matthew, Joachim Marti, et al. ‘Explicit Bias Toward High-Income-Country Research: A Randomized, Blinded, Crossover Experiment Of English Clinicians’. Health Affairs, vol. 36, no. 11, Nov. 2017, pp. 1997–2004. DOI.org (Crossref), https://doi.org/10.1377/hlthaff.2017.0773.

Harris, Matthew, James Macinko, et al. ‘Measuring the Bias against Low-Income Country Research: An Implicit Association Test’. Globalization and Health, vol. 13, no. 1, Nov. 2017, p. 80. BioMed Central, https://doi.org/10.1186/s12992-017-0304-y.

Pan, Raj Kumar, et al. ‘World Citation and Collaboration Networks: Uncovering the Role of Geography in Science’. Scientific Reports, vol. 2, no. 1, Nov. 2012, p. 902. www.nature.com, https://doi.org/10.1038/srep00902.

Price, Robyn, et al. ‘A Novel Data Solution to Inform Curriculum Decolonisation: The Case of the Imperial College London Masters of Public Health’. Scientometrics, vol. 127, no. 2, Feb. 2022, pp. 1021–37. Springer Link, https://doi.org/10.1007/s11192-021-04231-3.

Skopec, Mark, et al. ‘Decolonization in a higher education STEMM institution – is “epistemic fragility” a barrier?’ London Review of Education, vol. 19, no. 1, June 2021. journals.uclpress.co.uk, https://doi.org/10.14324/LRE.19.1.18.
# Contact
You can contact [Yusuf Ozkan](https://profiles.imperial.ac.uk/y.ozkan), Research Outputs Analyst for your questions.
