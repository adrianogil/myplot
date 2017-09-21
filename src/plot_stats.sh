
plot_folder_original='plot_template'
plot_folder='plot_stats'

rm -rf $plot_folder
cp -r $plot_folder_original $plot_folder

python plot_stats_data.py $1 $plot_folder