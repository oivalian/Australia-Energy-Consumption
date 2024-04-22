# Australia Monthly Energy Consumption (January 2011 - December 2021)
This was a small project I made for understanding pandas.
My original intention was to great a model that predicted energy usage over the next decade, which quickly evolved into a project that focused on data pre-processing, scrubbing and transformation.
Upon finalisation of the process, I decided to try utilize matplotlib to visualise the newly formulated data.

## Information
The original data set has been transformed and refined significanly. I dropped all countries except Australia, removed any irrelvant or unknown features. Some were in relation to storage and loss, others duplicated.
After selection, I aggregated the "PRODUCT" features into two seperate types: Fossil Fuels and Renewables.
I do intend on using this to make predictions on future consumption so watch this space.

### Dataset
ccanb23's [Monthly Electricity Production in GWh [2010-2022]](https://www.kaggle.com/datasets/ccanb23/iea-monthly-electricity-statistics) on [Kaggle](https://www.kaggle.com/).
The data itself has been scrapped from the [_International Energy Agency (IEA)_](iea.org/data-and-statistics/data-tools/monthly-electricity-statistics)

### Visual Observation
Upon applying visualisation, you can now see a clear trend toward renewables and a shift away from fossil fuels, though not nearly enough.

![image](https://github.com/oivalian/Australia-Energy-Consumption-January-2011---December-2021-/assets/109859213/84b9e35c-2957-49cc-a53e-c6f288e49ee5)
