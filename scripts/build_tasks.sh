cd tasks
shopt -s nullglob
dirlist=(*)
shopt -u nullglob # Turn off nullglob to make sure it doesn't interfere with anything later
echo "${dirlist[@]}"
for dir in ${dirlist[@]}
do
	cd $dir
	echo "Building $dir as qoa_framework_task_$dir ..."
	docker build -t "qoa_framework_task_$dir" .
	cd ../
done
