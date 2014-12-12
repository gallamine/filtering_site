# Time series filtering as a service

1. Create a filter (filter/new/?num_taps=XX&cutoff=0.5). Returns FID for accessing it in the future
2. Pass data into filter. (filter/run?fid=FID&data=comma-separated-list-of-numbers). Return output.
3. Get taps back from a filter (filter/taps?fid=FID
4. Get plots of the spectrum (filter/<fid>/plots/spectrum)
5. Get plots of the taps (filter/<fid>/plots/taps)