all:
	src/mkdata.py
	@mkdir -p plot
	src/plot.gpi

clean:
	rm -rf data.csv cycle.csv plot
