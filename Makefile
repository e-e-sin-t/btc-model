all:
	src/mkdata.py
	@mkdir -p plot/scale plot/zoom plot/future plot/ixic
	src/plot.gpi

clean:
	rm -rf data.csv cycle.csv plot
