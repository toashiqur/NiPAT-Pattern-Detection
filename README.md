# NiPAT- A Program Pattern Detection Tool

All programming languages need to be updated regularly by adding new features that fill programming needs. Existing approaches to determine new language features are completely manual and are based on language developers' experience, source code analysis, feature requests, and programmer interviews. Although these are acceptable practises, they are time-consuming and require a lot of brainstorming tasks, such as preparing interview questions, understanding ambiguous ideas, finding the common requirements, etc. No research, to our knowledge, has attempted to make the task of language feature identification easier. Through our research, we propose a systematic approach for identifying language features with the help of pattern and clone detection tools that work on source code. It semi-automates the task of feature identification, works quickly, and reduces the effort involved in existing practises. We identify features for the TXL language by implementing our idea and enabling the NiCAD clone detector to perform clone analysis on TXL source code, and developing a pattern detector. After detecting code patterns with the pattern detector and analyzing them, we propose eleven new features that can help improve the feature set of TXL.

The report on NiPAT can be downloaded from [Pattern analysis of TXL programs](https://ieeexplore.ieee.org/abstract/document/7476794/)

*Figure1. - An overview of NiPAT pattern detection process*
![]({{site.baseurl}}/assets/images/NipatProcess.png)

*Figure2. - Sample pattern found analyzing TXL programs by NiPAT*
![]({{site.baseurl}}/assets/images/samplePattern.png)


Tools: Python, XML, HTML, [TXL](https://www.txl.ca/txl-index.html), [NiCAD](https://www.txl.ca/txl-nicaddownload.html), Microsoft Visio
