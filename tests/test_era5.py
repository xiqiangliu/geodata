import logging

import geodata

logging.basicConfig(level=logging.INFO)


def get_data_configs() -> list[str]:
    return ["wind_solar_monthly"]


def get_bounds() -> list[list[int]]:
    return [[50, 0, 48, 3]]


def get_years() -> list[slice]:
    return [slice(2005, 2005)]


def get_months() -> list[slice]:
    return [slice(1, 2)]


def get_xs() -> list[slice]:
    return [slice(48.5, 49.5)]


def get_ys() -> list[slice]:
    return [slice(1, 2.5)]


def get_era5(data_config: str, bound: list[int], year: slice, month: slice):
    dataset = geodata.Dataset(
        module="era5",
        weather_data_config=data_config,
        years=year,
        months=month,
        bounds=bound,
    )
    if not dataset.prepared:
        dataset.get_data()
    return dataset


def create_cutout(data_config: str, x: slice, y: slice, year: slice, month: slice):
    cutout = geodata.Cutout(
        name="era5-europe-test-2005-01",
        module="era5",
        weather_data_config=data_config,
        xs=x,
        ys=y,
        years=year,
        months=month,
    )
    cutout.prepare()
    return cutout


def test_download():
    configs = get_data_configs()
    years = get_years()
    months = get_months()
    bounds = get_bounds()

    for config, year, month, bound in zip(configs, years, months, bounds):
        dataset = get_era5(config, bound, year, month)
        print(dataset)
        assert dataset


def test_cutout():
    configs = get_data_configs()
    years = get_years()
    months = get_months()
    xs = get_xs()
    ys = get_ys()

    for config, year, month, x, y in zip(configs, years, months, xs, ys):
        cutout = create_cutout(config, x, y, year, month)
        assert cutout.prepared
