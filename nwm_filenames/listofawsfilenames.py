from datetime import datetime
from dateutil import rrule
from itertools import product
import datetime


rundict = {
    1: "short_range",
    2: "medium_range",
    3: "medium_range_no_da",
    4: "long_range",
    5: "analysis_assim",
    6: "analysis_assim_extend",
    7: "analysis_assim_extend_no_da",
    8: "analysis_assim_long",
    9: "analysis_assim_long_no_da",
    10: "analysis_assim_no_da",
    11: "short_range_no_da",
}
memdict = {
    1: "mem_1",
    2: "mem_2",
    3: "mem_3",
    4: "mem_4",
    5: "mem_5",
    6: "mem_6",
    7: "mem_7",
}
vardict = {1: "channel_rt", 2: "land", 3: "reservoir", 4: "terrain_rt", 5: "forcing"}
geodict = {1: "conus", 2: "hawaii", 3: "puertorico"}
type = [
    ".CHRTOUT_DOMAIN1.comp",
    ".GWOUT_DOMAIN1.comp",
    ".LAKEOUT_DOMAIN1.comp",
    ".LDASOUT_DOMAIN1.comp",
    ".RTOUT_DOMAIN1.comp"
]
objecttype = [
    "forcing/",
    "model_output/"
]
def selectvar(vardict, varinput):
    return vardict[varinput]
def selectgeo(geodict, geoinput):
    return geodict[geoinput]
def selectrun(rundict, runinput):
    return rundict[runinput]
import requests

def makename(
        date,
        run_name,
        var_name,
        fcst_cycle,
        fcst_hour,
        geography,
        run_type,
        fhprefix="",
        runsuffix="",
        varsuffix="",
        run_typesuffix="",
        urlbase_prefix="",
):
    datetxt = f"nwm.{date.strftime('%Y%m%d')}"
    foldertxt = f"{run_type}{run_typesuffix}"
    filetxt = f"nwm.t{fcst_cycle:02d}z.{run_name}{runsuffix}.{var_name}{varsuffix}.{fhprefix}{fcst_hour:03d}.{geography}.nc"
    url = f"{urlbase_prefix}{datetxt}/{foldertxt}/{filetxt}"

    # Check if the link exists
    response = requests.head(url)
    if response.status_code == 200:
        return url
    else:
        return None



def makename2(
        date,
        object_type,
        urlbase_prefix,
        typeinput,
):
    yeartxt = f"{date.strftime('%Y')}"
    datetxt = f"{date.strftime('%Y%m%d%H')}"
    urlbase_prefix = urlbase_prefix + objecttype[object_type - 1]

    if yeartxt == "2020":
        url = f"{urlbase_prefix}{yeartxt}/{datetxt}00{type[typeinput - 1]}"
    else:
        url = f"{urlbase_prefix}{yeartxt}/{datetxt}00.LDASIN_DOMAIN1"

    # Check if the link exists
    response = requests.head(url)
    if response.status_code == 200:
        return url
    else:
        return None

# setting run_type
def run_type(runinput, varinput, geoinput, default=""):
    if varinput == 5:  # if forcing
        if runinput == 5 and geoinput == 2:  # if analysis_assim and hawaii
            return "forcing_analysis_assim_hawaii"
        elif runinput == 5 and geoinput == 3:  # if analysis_assim and puerto rico
            return "forcing_analysis_assim_puertorico"
        elif runinput == 1 and geoinput == 2:  # if short range and hawaii
            return "forcing_short_range_hawaii"
        elif runinput == 1 and geoinput == 3:  # if short range and puerto rico
            return "forcing_short_range_puertorico"
        elif runinput == 5:  # if analysis assim
            return "forcing_analysis_assim"
        elif runinput == 6:  # if analysis_assim_extend
            return "forcing_analysis_assim_extend"
        elif runinput == 2:  # if medium_range
            return "forcing_medium_range"
        elif runinput == 1:  # if short range
            return "forcing_short_range"
    elif runinput == 5 and geoinput == 3:  # if analysis_assim and puertorico
        return "analysis_assim_puertorico"
    elif runinput == 10 and geoinput == 3:  # if analysis_assim_no_da and puertorico
        return "analysis_assim_puertorico_no_da"
    elif runinput == 1 and geoinput == 3:  # if short_range and puerto rico
        return "short_range_puertorico"
    elif runinput == 11 and geoinput == 3:  # if short_range_no_da and puerto rico
        return "short_range_puertorico_no_da"
    else:
        return default
def fhprefix(runinput):
    if 4 <= runinput <= 10:
        return "tm"
    return "f"
def varsuffix(meminput):
    if meminput in range(1, 8):
        return f"_{meminput}"
    else:
        return ""
def run_typesuffix(meminput):
    if meminput in range(1, 8):
        return f"_mem{meminput}"
    else:
        return ""
def select_forecast_cycle(fcst_cycle=None, default=None):
    if fcst_cycle:
        return fcst_cycle
    else:
        return default
def select_lead_time(lead_time=None, default=None):
    if lead_time:
        return lead_time
    else:
        return default
urlbasedict = {
    0: "",
    1: "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/prod/",
    2: "https://nomads.ncep.noaa.gov/pub/data/nccf/com/nwm/post-processed/WMS/",
    3: "https://storage.googleapis.com/national-water-model/",
    4: "https://storage.cloud.google.com/national-water-model/",
    5: "gs://national-water-model/",
    6: "https://noaa-nwm-retrospective-2-1-pds.s3.amazonaws.com/",
    7: "s3://noaa-nwm-retrospective-2-1-pds/model_output/",
}
def selecturlbase(urlbasedict, urlbaseinput, objecttype=1, defaulturlbase=""):
    if urlbaseinput:
        return urlbasedict[urlbaseinput]
    else:
        return defaulturlbase


def validate_date_range(start_date, end_date):
    try:
        if len(start_date) != 12 or len(end_date) != 12:
            raise ValueError("No File Names present in the given year range")

        try:
            start_date_year = int(start_date[:4])
            start_date_month = int(start_date[4:6])
            start_date_day = int(start_date[6:8])
            datetime.datetime(start_date_year, start_date_month, start_date_day)

            end_date_year = int(end_date[:4])
            end_date_month = int(end_date[4:6])
            end_date_day = int(end_date[6:8])
            datetime.datetime(end_date_year, end_date_month, end_date_day)

            _dtstart = datetime.datetime.strptime(start_date, "%Y%m%d%H%M")
            _until = datetime.datetime.strptime(end_date, "%Y%m%d%H%M")
            _starttime = datetime.datetime.strptime(start_date[8:], "%H%M")
            _endtime = datetime.datetime.strptime(end_date[8:], "%H%M")

            if _starttime.hour < 0 or _starttime.hour > 23 or _endtime.hour < 0 or _endtime.hour > 23:
                raise ValueError("Incorrect time range entered. Time range should be between 0000 - 2300 (HHMM).")

        except ValueError:
            raise ValueError("Start and end dates should be in format 'YYYYMMDD'.")

    except ValueError as ve:
        raise ve

    return _dtstart, _until, _starttime, _endtime


def create_file_list(
        runinput,
        varinput,
        geoinput,
        meminput,
        start_date=None,
        end_date=None,
        fcst_cycle=None,
        urlbaseinput=None,
        lead_time=None,  # TODO: change this order; placed here to avoid breaking change
        type=[1],
        objecttype=None
):
    # for given date,  run, var, fcst_cycle, and geography, print file names for the valid time (the range of fcst_hours) and dates
    runsuff = ""
    try:
        geography = selectgeo(geodict, geoinput)
    except:
        geography = "geography_error"
    try:
        run_name = selectrun(rundict, runinput)
    except:
        run_name = "run_error"
    try:
        var_name = selectvar(vardict, varinput)
    except:
        var_name = "variable_error"
    try:
        urlbase_prefix = selecturlbase(urlbasedict, urlbaseinput)
    except:
        urlbase_prefix = "urlbase_error"

    valid_types = [1, 2, 3, 4, 5]
    if not all(x in valid_types for x in type):
        raise ValueError("Invalid type input. Type can be any combination of [1, 2, 3, 4, 5].")

    r = []
    if urlbaseinput != 6:
        _dtstart, _until, _starttime, _endtime = validate_date_range(start_date, end_date)

        '''
        except:
            today = datetime.now(timezone.utc)
            _dtstart = today
            _until = today
        '''
        dates = rrule.rrule(
            rrule.DAILY,
            dtstart=_dtstart,
            until=_until,
        )
        run_t = run_type(runinput, varinput, geoinput, run_name)
        fhp = fhprefix(runinput)
        vsuff = varsuffix(meminput)
        rtsuff = run_typesuffix(meminput)

        if runinput == 1:  # if short_range
            if varinput == 5:  # if forcing
                if geoinput == 2:  # hawaii
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, range(0, 13, 12)),
                        select_lead_time(lead_time, range(1, 49)),
                    )
                elif geoinput == 3:  # puertorico
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, [6]),
                        select_lead_time(lead_time, range(1, 48)),
                    )
                else:
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, range(24)),
                        select_lead_time(lead_time, range(1, 19)),
                    )
            elif geoinput == 3:  # if puerto rico
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(6, 19, 12)),
                    select_lead_time(lead_time, range(1, 48)),
                )
            else:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(24)),
                    select_lead_time(lead_time, range(1, 19)),
                )
        elif runinput == 2:  # if medium_range
            if varinput == 5:  # if forcing
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(0, 19, 6)),
                    select_lead_time(lead_time, range(1, 241)),
                )
            else:
                default_fc = range(0, 19, 6)
                if meminput == 1:
                    if varinput in {1, 3}:
                        prod = product(
                            dates,
                            select_forecast_cycle(fcst_cycle, default_fc),
                            select_lead_time(lead_time, range(1, 241)),
                        )
                    elif varinput in {2, 4}:
                        prod = product(
                            dates,
                            select_forecast_cycle(fcst_cycle, default_fc),
                            select_lead_time(lead_time, range(3, 241, 3)),
                        )
                    else:
                        raise ValueError("varinput")
                elif meminput in range(2, 8):
                    if varinput in {1, 3}:
                        prod = product(
                            dates,
                            select_forecast_cycle(fcst_cycle, default_fc),
                            select_lead_time(lead_time, range(1, 205)),
                        )
                    elif varinput in {2, 4}:
                        prod = product(
                            dates,
                            select_forecast_cycle(fcst_cycle, default_fc),
                            select_lead_time(lead_time, range(3, 205, 3)),
                        )
                    else:
                        raise ValueError("varinput")
                else:
                    raise ValueError("meminput")
        elif runinput == 3:  # if medium_range_no_da
            if varinput == 1:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(0, 13, 6)),
                    select_lead_time(lead_time, range(3, 240, 3)),
                )
            else:
                raise ValueError("only valid variable for a _no_da type run is channel_rt")
        elif runinput == 4:  # if long_range
            default_fc = range(0, 19, 6)
            if varinput in {1, 3}:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, default_fc),
                    select_lead_time(lead_time, range(6, 721, 6)),
                )
            elif varinput == 2:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, default_fc),
                    select_lead_time(lead_time, range(24, 721, 24)),
                )
            else:
                raise ValueError("varinput")
        elif runinput == 5:  # if analysis_assim (simplest form)
            if varinput == 5:  # if forcing
                if geoinput == 2:  # hawaii
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, range(19)),
                        select_lead_time(lead_time, range(3)),
                    )
                else:
                    prod = product(
                        dates,
                        select_forecast_cycle(fcst_cycle, range(20)),
                        select_lead_time(lead_time, range(3)),
                    )
            else:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(24)),
                    select_lead_time(lead_time, range(3)),
                )
        elif runinput == 6:  # if analysis_assim_extend
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, [16]),
                select_lead_time(lead_time, range(28)),
            )
        elif runinput == 7:  # if analysis_assim_extend_no_da
            if varinput == 1:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, [16]),
                    select_lead_time(lead_time, range(28)),
                )
            else:
                raise ValueError("only valid variable for a _no_da type run is channel_rt")
        elif runinput == 8:  # if analysis_assim_long
            prod = product(
                dates,
                select_forecast_cycle(fcst_cycle, range(0, 24, 6)),
                select_lead_time(lead_time, range(12)),
            )
        elif runinput == 9:  # if analysis_assim_long_no_da
            if varinput == 1:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(0, 24, 6)),
                    select_lead_time(lead_time, range(12)),
                )
            else:
                raise ValueError("only valid variable for a _no_da type run is channel_rt")

        elif runinput == 10:  # if analysis_assim_no_da
            if varinput == 1:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(21)),
                    select_lead_time(lead_time, range(3)),
                )
            else:
                raise ValueError("only valid variable for a _no_da type run is channel_rt")

        elif runinput == 11 and geoinput == 3:  # if short_range_puertorico_no_da
            if varinput == 1:
                prod = product(
                    dates,
                    select_forecast_cycle(fcst_cycle, range(6, 19, 12)),
                    select_lead_time(lead_time, range(1, 49)),
                )
            else:
                raise ValueError("only valid variable for a _no_da type run is channel_rt")
        else:
            raise ValueError("run error")
        for _dt, _fc, _fh in prod:
            file_name  = makename(
                    _dt,
                    run_name,
                    var_name,
                    _fc,
                    _fh,
                    geography,
                    run_t,
                    fhp,
                    runsuff,
                    vsuff,
                    rtsuff,
                    urlbase_prefix,
                )
            if file_name is not None:
                r.append(file_name)
    else:
        _dtstart1, _until1, _starttime, _endtime = validate_date_range(start_date, end_date)
        dates1 = rrule.rrule(
            rrule.HOURLY,
            dtstart=_dtstart1,
            until=_until1,
        )

        if isinstance(objecttype, int):
            objecttype = [objecttype]

        if not all(x in [1, 2] for x in objecttype):
            raise ValueError("Invalid object type. Valid object types are 1, 2, or both [1, 2].")

        datetimes = product(
            dates1,
            range(1)
        )
        for _dt, th in datetimes:
            for tp in type:
                for obj_type in objecttype:
                    file_name  = makename2(
                            _dt,
                            obj_type,
                            urlbase_prefix,
                            tp,
                        )
                    if file_name is not None:
                        r.append(file_name)
    return r,len(r)

def main():
    start_date = "20200101"
    end_date = "20200102"
    fcst_cycle = [12, 18]
    lead_time = [1, 2, 240]
    # fcst_cycle = None  # Retrieves a full day for each day within the range given.
    runinput = 2
    varinput = 1
    geoinput = 1
    meminput = 1
    urlbaseinput = 6
    start_time = "0000"
    end_time = "0600"
    type_input = [5]
    object_type = 1,2
    try:
        file_list,length = create_file_list(
            runinput,
            varinput,
            geoinput,
            meminput,
            start_date + start_time,
            end_date + end_time,
            fcst_cycle,
            urlbaseinput,
            lead_time,
            type_input,
            object_type
        )
        if(length == 0):
            print(f"No files found")
        else:
            print(f"Files: {file_list}\nTotal files: {length}")
    except ValueError as ve:
        print(ve)

if __name__ == "__main__":
    main()
