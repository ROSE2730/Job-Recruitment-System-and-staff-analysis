import pickle
from flask import request, Flask, render_template, redirect, url_for, flash


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


app = Flask(__name__)

# loading models-------------------------
df = pd.read_csv("notebooks/HR_comma_sep.csv")
model = pickle.load(open('models/model.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))

# dashboard functions-----------------------------
def reading_cleaning(df):
    df.drop_duplicates(inplace=True)
    cols = df.columns.tolist()
    df.columns = [x.lower() for x in cols]

    return df


df = reading_cleaning(df)


def employee_important_info(df):
    average_satisfaction = df['satisfaction_level'].mean()
    department_satisfaction = df.groupby('department')['satisfaction_level'].mean()
    salary_satisfaction = df.groupby('salary')['satisfaction_level'].mean()

    left_employees = len(df[df['left'] == 1])

    stayed_employees = len(df[df['left'] == 0])

    return average_satisfaction, department_satisfaction, salary_satisfaction, left_employees, stayed_employees


def plots(df, col):
    values = df[col].unique()
    plt.figure(figsize=(15, 8))

    explode = [0.1 if len(values) > 1 else 0] * len(values)
    plt.pie(df[col].value_counts(), explode=explode, startangle=40, autopct='%1.1f%%', shadow=True)
    labels = [f'{value}({col})' for value in values]
    plt.legend(labels=labels, loc='upper right',fontsize=12)
    plt.title(f'distribution of {col}',fontsize=16,fontweight='bold')

    plt.savefig('static/' + col + '.png')
    plt.close()


def distribution(df, col):
    values = df[col].unique()
    plt.figure(figsize=(15, 8))
    sns.countplot(x=df[col], hue='left', palette='Set1', data=df)
    labels = [f'{val} ({col})' for val in values]
    plt.legend(labels=labels, loc='upper right',fontsize=12)
    plt.title('distribution of {col}',fontsize=16,fontweight='bold')
    plt.xticks(rotation=90)
    plt.savefig('static/'+col+'distribution.png')
    plt.close()


def comparison(df, x, y):
    plt.figure(figsize=(15, 10))
    sns.barplot(x=x, y=y, hue="left", data=df, ci=None)
    plt.title(f'{x} vs {y}', fontsize=10, fontweight='bold')
    plt.savefig('static/comparison.png')
    plt.close()


def corr_with_left(df):
    df_encoded = pd.get_dummies(df)
    correlations = df_encoded.corr()['left'].sort_values()[::-1]
    colors = ['skyblue' if corr > 0 else 'salmon' for corr in correlations]

    plt.figure(figsize=(15, 10))
    correlations.plot(kind='barh', color=colors)

    plt.title('Correlation with Left', fontsize=16, fontweight='bold')
    plt.xlabel('Correlation', fontsize=14, fontweight='bold')
    plt.ylabel('Features', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('static/correlation.png')
    plt.close()


def histogram(df, col):
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))  # Create a grid of 1 row and 2 columns

    # Plot the first histogram
    sns.histplot(data=df, x=col, hue='left', bins=20, ax=axes[0])
    axes[0].set_title(f'Histogram of {col}', fontsize=10, fontweight='bold')

    # Plot the second histogram
    sns.kdeplot(data=df, x='satisfaction_level', y='last_evaluation', hue='left', shade=True, ax=axes[1])
    axes[1].set_title('Kernel Density Estimation', fontsize=10, fontweight='bold')

    plt.tight_layout()  # Adjust the layout to prevent overlapping
    plt.savefig('static/' + col + 'satisfaction_level_histogram.png')
    plt.close()






#prediction_function----------------------------
def prediction(sl_no, gender, ssc_p, hsc_p, degree_p, work_exp, etest_p, specialisation, mba_p):
    data = {
        'sl_no': [sl_no],
        'gender': [gender],
        'ssc_p': [ssc_p],
        'hsc_p': [hsc_p],
        'degree_p': [degree_p],
        'work_exp': [work_exp],
        'etest_p': [etest_p],
        'specialisation': [specialisation],
        'mba_p': [mba_p]
    }

    data = pd.DataFrame(data)
    data['gender'] = data['gender'].map({'Male': 1, 'Female': 0})
    data['work_exp'] = data['work_exp'].map({'Yes': 1, 'No': 0})
    data['specialisation'] = data['specialisation'].map({'Mkt&HR': 1, 'Mkt&Fin': 0})
    scaled_df = scaler.transform(data)
    result=model.predict(scaled_df).reshape(1,-1)
    return result[0]


#routes---------------------------------

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/index")
def index():
    return render_template('index.html')
@app.route("/job")
def job():
    return render_template('job.html')
@app.route("/ana")
def ana():
    average_satisfaction, department_satisfaction, salary_satisfaction, left_employees, stayed_employees = employee_important_info(df)
    plots(df,'left')
    plots(df,'salary')
    plots(df,'number_project')
    plots(df,'department')

    #call distribution
    distribution(df,'salary')
    distribution(df,'department')

    #call comaprison function
    comparison(df,'department','satisfaction_level')

    #call correlation function
    corr_with_left(df)

    histogram(df,'satisfaction_level')

    department_satisfaction = department_satisfaction.to_dict()
    salary_satisfaction = salary_satisfaction.to_dict()
    return render_template(
        'ana.html',
        df=df.head(),  # Convert DataFrame to HTML
        average_satisfaction=average_satisfaction,
        department_satisfaction=department_satisfaction,
        salary_satisfaction=salary_satisfaction,
        left_employees=left_employees,
        stayed_employees=stayed_employees
    )



# prediction------------------------------

@app.route('/placement', methods=['POST', 'GET'])
def placement():
    if request.method == 'POST':
        sl_no = request.form['sl_no']
        gender = request.form['gender']
        ssc_p = request.form['ssc_p']
        hsc_p = request.form['hsc_p']
        degree_p = request.form['degree_p']
        work_exp = request.form['work_exp']
        etest_p = request.form['etest_p']
        specialisation = request.form['specialisation']
        mba_p = request.form['mba_p']


        result = prediction(sl_no, gender, ssc_p, hsc_p, degree_p, work_exp, etest_p, specialisation,mba_p)

        if result == 1:
            pred = "Placed"
            rec = "We recommend you that this is the best candidate for your business"
            return render_template('job.html', result=pred, rec=rec)
        else:
            pred = "Not Placed"
            rec = "We recommend you that this is not the best candidate for your business"
            return render_template('job.html', result=pred, rec=rec)


if __name__ == "__main__":
    app.run(debug=True)