SELECT
	year(tgdp),
    (renen.annualproduction / (pren.annualsupply*1000))*100  AS perc_renen,
	annualemissions(co2),
	countryname(cc),
	countrycode(cc)

FROM
	project.gdp AS tgdp,
	project.primaryenergy AS pren,
	project.renewableenergy AS renen,
	project.commoncountries AS cc,
    project.co2emissions AS co2

WHERE
	tgdp.countrycode = cc.countrycode
	AND renen.countrycode = cc.countrycode
	AND pren.countrycode = cc.countrycode
	AND tgdp.year = renen.year
	AND renen.year = pren.year
    AND co2.year = pren.year
    AND co2.countrycode = cc.countrycode