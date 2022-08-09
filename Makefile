all:
	./mkdata.py
	@mkdir -p plot
	./plot.gpi

clean:
	rm -rf data.csv cycle.csv plot
