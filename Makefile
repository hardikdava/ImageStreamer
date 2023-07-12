.PHONY: style check_code_quality

export PYTHONPATH = .
check_dirs := image_streamer

style:
	black  $(check_dirs)
	isort --profile black $(check_dirs)