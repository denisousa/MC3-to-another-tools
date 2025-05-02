# Static Code Analysis Alarms Filtering Reloaded: an ML Approach and its Empirical Evaluation on a New Real-World Dataset

### Replication Data Package

------

#### Background

This document describes the content of a replication data package for a paper titled "*Static Code Analysis Alarms Filtering Reloaded: an ML Approach and its Empirical Evaluation on a New Real-World Dataset*". 

<u>Paper abstract:</u> Even though Static Code Analysis (SCA) tools are integrated into many modern software building and testing pipelines, their practical impact is still seriously hindered by the excessive number of false positive warnings they usually produce. To cope with this problem, researchers have proposed several post-processing methods that aim to filter out false hits (or equivalently identify ``actionable'' warnings) after the SCA tool produced its results. However, we found that most of these approaches are targeted (i.e., deal with only a few SCA warning types) and evaluated on synthetic benchmarks or small-scale manually collected data sets (i.e., with typical sample sizes of several hundred).

In this paper, we present a code embedding-based approach for filtering false positive warnings produced by 160 different SonarQube rule checks, one of the most widely adopted SCA tools today. We evaluate the method on a dataset containing 224,484 real-world warning samples fixed (true positive samples) or ignored (false positive samples) by the developers, which we collected from 9,958 different open-source Java projects from GitHub using a data mining approach. It is the most extensive real-world study and public dataset we know of in this area. Our method works with an accuracy of 91% (best F1-score of 81.3% and AUC of 95.3%) for the classification of SonarQube warnings.

#### Dataset Description

The data package contains the data collected from GitHub using a data mining approach. Besides the main csv training data that consists of 224,484 learning samples (47,015 true positive SonarQube warnings and 177,469 false positives), the package also provides the raw data from which the final dataset is derived. It includes the Java source code files containing either a true positive warning that has been fixed by the developers or false positives, namely files containing the "\\\NOSONAR" commit ignoring a SonarQube warning. We also provide the fix patches for true positive instances and the list of identified SonarQube alerts for the lines ignored by "\\\NOSONAR" in false positive cases. Additionally, result statistics, charts, and pre-trained word2vec models are also available in the package.

#### Detailed Package Contents

The data package contains the following files and folders:

* `main_dataset.csv` - the main data table for the ML models. Each row represents a SonarQube warning that is either fixed (true positive, class label 0) or ignored (false positive, class label 1). The remaining columns mark the actual warning type (squid), the original code context (source code line with the alarm and its preceding and succeeding 2 lines) and the tokenized form of the code context. *Note:* the data table cannot be fed into an ML model directly as one needs to compute the average word2vec vectors for the lines. The word2vec language model is available under the `gensim` folder. A sample data split with the actual vectors can be found in the `input` folder.
* `charts` - figures generated from the data and/or results.
  * `hyperparam` - figures related to hyperparameter search.
  * `squid-distribution.xlsx` - the total number and distribution of the true positive and false positive SonarQube warning instances in the collected dataset.
  * `tokens_with_numbers.png` - the frequency of code tokens used for the word2vec embedding.
  * `test_results.png` - the prediction accuracy of the RForest model per SonarQube warning type.
* `raw_data` - raw data collected from GitHub using a data mining process.
  * `false_positives` - the raw data for false positive SonarQube warnings.
    * `fp_complete.csv` - a raw csv containing the false positive samples. Each row marks a false positive squid. The csv columns contain the GitHub repository and exact version (sha hash) of the affected file, the type of squid and the location of the "\\\\NOSONAR" comment within the file. We reveal the type of omitted SonarQube warning by temporarily removing the "\\\\NOSONAR" comment and running a SonarQube analysis on the file to find out the issued warnings to the line in question.
    * `original_files.7z` - for archival reasons, we do not only provide the GitHub url for the files  but also publish their downloaded versions. This compressed package contains all the original files with the proper versions containing a "\\\\NOSONAR" comment (these files are referred to in the `fp_complete.csv`).
  * `true_positives` - the raw data for true positive SonarQube warnings.
    * `tp_complete.csv` - a raw csv containing the true positive samples. Each row marks a true positive squid. The csv columns contain the GitHub repository and exact version of the original (orig_sha) and fixed (fix_sha) versions of the affected file, the type of squid and its location within the file. The csv also contains a reference to the patch file containing the fix to this issue (stored in `patches.7z`).
    * `original_files.7z` - for archival reasons, we do not only provide the GitHub url for the files  but also publish their downloaded versions. This compressed package contains all the original files with the proper versions containing a squid that the developers fixed (these files are referred to in the `tp_complete.csv`).
    * `patches.7z` - for archival reasons, we also downloaded and published the identified code changes that fix the squid present in the original source files. This compressed package contains all the squid fixing patches (these files are referred to in the `tp_complete.csv`).
* `gensim` - the dumped word2vec language model generated with gensim.
* `input` - a sample data split to train and test with the actual vectors.
* `results` - the 10-fold cross-validation results for the four ML models with the best hyperparameters. The results are stored as a Python dictionary in a dumped pickle file (`best_10fold_metrics.pkl`) that can be printed out with the provided `dump_metrics.py` file or processed with other Python scripts. The per type accuracy measures can be found in the ``results_by_types.csv`` file.
* `systems.txt` - the list of final GitHub subject systems (where we collected the true and false positive samples from).
* `README.md` - this document.



"# MC3-to-another-tools" 
