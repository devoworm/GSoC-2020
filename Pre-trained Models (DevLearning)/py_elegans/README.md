## py_elegans 

> Still under construction

Importing a model for inferences 

1. `from pyelegans import lineage_population_model`

Loading a model instance to be used to estimate lineage populations of embryos from videos/photos.

2. `model = lineage_population_model(mode = "cpu")`

Making a prediction from an image

3. `pred = (model.predict(image_path = "sample.png"))`

Making predictions from a video and saving the predictions into a CSV file

4. `results = model.predict_from_video(video_path = "sample_videos/20090309_F39B2_1_7_L1.mov", save_csv = True, csv_name = "foo.csv" )
`
