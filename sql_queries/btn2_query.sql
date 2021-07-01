SELECT
	year(tgdp),
	(gdp(tgdp) / population(c)) AS gdp_per_capita,
	(renen.annualproduction / (pren.annualsupply*1000))*100  AS perc_renen,
	countryname(cc)

FROM
	project.gdp AS tgdp,
	project.primaryenergy AS pren,
	project.renewableenergy AS renen,
	project.commoncountries AS cc,
	project.country AS c

WHERE
	tgdp.countrycode = cc.countrycode
	AND renen.countrycode = cc.countrycode
	AND pren.countrycode = cc.countrycode
	AND tgdp.year = renen.year
	AND renen.year = pren.year
	AND tgdp.year = c.year
	AND cc.countryname = c.countryname