# Group Lines by connectivity.
Useful for grouping shaffled lines before supplying to PolyCurve.ByJoinedCurves node.
___
- Supply: list of lines.
- Returns: list of lines, grouped by connectivity (have common point).
___
- Script does not check for duplicated lines or possible branches (when more than two lines share one point). Do it yourself before or after grouping!
- Script does not flip or sort the lines for chaining.
___
Tested with Dynamo 2.12
