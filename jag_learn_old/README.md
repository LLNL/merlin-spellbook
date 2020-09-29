An example workflow running the jag model through a spec file.
The workflow submits tasks to run various samples through jag,
collects the individual results, translates them to a numpy array,
builds a random forest surrogate model, and makes a prediction on
new samples.

# Quick Start

This will submit the tasks and then stand up workers:

    merlin run jag_learn.yaml
    merlin run-workers jag_learn.yaml

# Components

    # Ensemble file that puts it all together
    jag_learn.yaml

    # Things for jag
    jag_exe.py       # a stand-alone jag executible
    jag_params.py    # parameters read in by jag

    # Things for machine learning
    learn.py         # a random-forest learner
    predict.py       # a predictor that evaluates the learned model on new samples

    # Things for sampling
    make_samples.py  # a sample generator, which can scale the outputs between (min,max)

    # Things for data processing
    collector.cxx    # c++ program for collecting lots of .hdf5 files into a single one
    features.json    # file that says what features to collect from the .hdf5 files
    translator.py             # translates flat sample-based .hdf5 into arrays in .npz (or .json, .hdf5, .conduit_bin)
    features_translate.json   # file that says which features to put into the .npz file 
