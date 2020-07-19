from pyelegans import lineage_population_model

model = lineage_population_model(mode = "cpu")

print(model.predict(image_path = "sample.png"))

results = model.predict_from_video(video_path = "sample_videos/20090309_F39B2_1_7_L1.mov", save_csv = True, csv_name = "foo.csv" )