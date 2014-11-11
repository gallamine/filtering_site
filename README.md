# Time series filtering as a service

1. Create a filter (filter/new/?config={}). Returns FID for accessing it in the future
2. Pass data into filter. (filter/<fid>/run?data=comma-separated-list-of-numbers). Return output.
3. Get taps back from a filter (filter/<fid>/taps
4. Get plots of the spectrum (filter/<fid>/plots/spectrum)
5. Get plots of the tabps (filter/<fid>/plots/taps)