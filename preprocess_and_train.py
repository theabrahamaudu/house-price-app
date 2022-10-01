import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
import joblib


def preprocess(filepath):
    try:
        housing_data = pd.read_csv(filepath)

        # Dealing with outliers
        # Trim off the top and bottom 15th percentile of data by price
        q1, q9 = housing_data['price'].quantile([0.15, 0.85])
        mask_df = housing_data['price'].between(q1, q9)
        new_data = housing_data[mask_df]

        # Rename columns
        new_data.rename(columns={'title': 'house_type'}, inplace=True)

        # remove states with very few records
        few_records = new_data['state'].value_counts()
        new_data = new_data[~new_data['state'].isin(few_records[few_records < 20].index)]

        # reset the dataframe index
        new_data.reset_index(inplace=True)
        del new_data['index']

        new_data.to_csv('preprocessed_data.csv', index=False)

        print('Data preprocessed successfully')
        return new_data
    except Exception as e:
        print('There was an error preprocessing the data: \n', e)


def linear_regression_model(new_data):
    # Get categorical features
    categorical_features = [feature for feature in new_data.columns if new_data[feature].dtypes == 'O']

    X = new_data.drop(['price'], axis=1)
    y = new_data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=828)

    # OneHotEncoding
    ohe = OneHotEncoder()
    ohe.fit(X[categorical_features])
    column_trans = make_column_transformer((OneHotEncoder(categories=ohe.categories_),
                                            categorical_features), remainder='passthrough')

    # Initailize Regresion Model
    reg = LinearRegression()

    # Make a pipeline
    pipe = make_pipeline(column_trans, reg)

    # fit the model
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    # Save the model
    joblib.dump(pipe, open('LinearRegressionModel.joblib', 'wb'))

    score = r2_score(y_test, y_pred)
    print(f"Linear Regression Model R2 Score: ", score)
    return score


if __name__=="__main__":
    filepath = 'nigeria_housing_dataset.csv'
    new_data = preprocess(filepath=filepath)
    LR_model = linear_regression_model(new_data=new_data)
