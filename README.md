# unemployment_prediction
ML project about the uneployment rate in each state. This is a Project for mlzoomcamp course by Datatalks ( https://datatalks.club/ )

![](images.jpg)

---

## 1 - Problem description

The unemployed are people of working age who are without work, they are available for work, and they have taken specific steps to find work. 
This indicator is measured in numbers of unemployed people as a percentage of the labour force and it is seasonally adjusted. The labour force is defined as the total number of unemployed people plus those in employment.

---
## 2 - The Goal

The target of this project is to predict the current value of the unemployed for each state, based on economic national data.

--- 

## 3 - Data

The data was obtained from this repository which processed the data from https://data.worldbank.org/ : 
https://www.kaggle.com/datasets/mittvin/world-economic-indicators-1960-2022-dataset

Important details about the data:
- Country Name: A string indicating the name of the country.
- Country Code: A three-letter code uniquely identifying each country.
- Year: The year to which the data corresponds.
- Personal Remittances, Received (% of GDP): The percentage of Gross Domestic Product (GDP) that a country receives in the form of personal remittances from individuals living abroad.
- Unemployment, Total (% of Total Labor Force): The percentage of the total labor force that is unemployed and actively seeking employment.
- GDP (current US$): The Gross Domestic Product (GDP) of the country in current US dollars, representing the total value of all goods and services produced within the country's borders.
- GDP Growth (Annual %): The annual percentage increase in Gross Domestic Product (GDP) from the previous year.
- GDP (current US$): Another measure of Gross Domestic Product (GDP) in current US dollars, potentially from a different source or calculation.
- GDP Growth (Annual %): Another measure of the annual percentage increase in Gross Domestic Product (GDP) from the previous year, potentially from a different source or calculation.

I uploaded the entire dataset to the repository. File: *world_economic_indicators.csv* in the data directory.
This data is processed using the ``train.py`` file, that creates the model ``.bin``.

After EDA, i decided to delete some columns based on the redundant value already present in the dataset. I cut:
- Country Name: info already present in the country code.
- GDP Growth (Annual %): info already present in another column.
- GDP (current US$): info already present in another column. 

---

## 4 - Structure of the repository

### DATASET
- **world_economic_indicators.csv**: contains the full dataset, it is in folder named 'data'

### Files
- **CapstoneProj2.ipynb**: contains the notebook to explore the data and choose the model with the best results
- **Pipfile and Pipfile.lock**: contains the dependencies to run the repo
- **predict.py**: contains the prediction using flask
- **test.py**: contains some values to test the model
- **train.py**: contains the model with the best performance in the testing set, obtained using the notebook
- **Dockerfile**: contains the image for the docker

---
## 5 - Loading final model into a service:

#### pipenv 

The script *train.py* create the model : *unemployment.bin* and it can run in a separate virtual environment across its dependency files *Pipenv* and *Pipenv.lock*.
*flask* was used for the local deployment in *train.py* script.

- Install pipenv :
```
pip install pipenv
```
- Get a copy of project and dependencies, or clone the repository :
```
git clone https://github.com/bergimax/unemployment_prediction/
```
- From the project's folder, run :
``` 
pipenv install
```
- All the dependencies should be automatically soddisfied, just verify.

- From the project's folder, run :
``` 
python train.py
```
Now it has to build the model ''.bin'', give it some time. 

- After the model's creation, run the local service using gunicorn inside the virtual environment:
```
pipenv run gunicorn --bind 0.0.0.0:9696 predict:app
```

#### Docker
There is also the file: *Dockerfile* in the repository, through this you can run the service in a completely separate container. To run the Docker, be sure your docker service is running. If you are using wsl2 on Windows, to run the build command you need to make sure your docker dekstop is running, otherwise you will get an error. 
For the docker, you have to:

- From the project directory, create the docker image :
```
docker build -t unemployment .
```
- Run the docker image created:
```
docker run -it --rm -p 9696:9696 unemployment:latest
```
The build command can take several minutes to run. Just give it time.

#### Test the local service:

- To test the local service, you can run the test script in another terminal:
```
python test.py
```
- If you edit the values to analize some data, you should modify the parameters in the file test.py, maybe you cane take them from the smaller dataset present in this repo of each market. To do it, you should do the command:
```
vi test.py
```
P.S: The current values in test.py are taken from the dataset, raw number 16608, for the Italy, my country.

---
