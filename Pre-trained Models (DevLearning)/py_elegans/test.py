from pyelegans import lineage_population_model

model = lineage_population_model(mode = "cpu")

print(model.predict(image_path = "sample_data/sample.png"))

results = model.predict_from_video(video_path = "sample_data/sample_videos/20090309_F39B2_1_7_L1.mov", save_csv = True, csv_name = "sample_preds/video_preds.csv", ignore_first_n_frames= 10, ignore_last_n_frames= 10 )
                                    
plot = model.create_population_plot_from_video(video_path = "sample_data/sample_videos/20090309_F39B2_1_7_L1.mov", save_plot= True, plot_name= "sample_preds/plot.png", ignore_last_n_frames= 30 )
plot.grid()
plot.show()