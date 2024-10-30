# 📚 Book Recommendation System Project

## 🎯 Objective

The goal of this project is to build a **Book Recommendation System** for users. Effective recommendation systems are crucial in many industries as they can significantly increase revenue and differentiate a platform from competitors.

---

## 🛠️ Methods Used

- **📊 Descriptive Statistics**
- **📈 Data Visualization**
- **🤖 Machine Learning**

## 💻 Technologies

- **Python**
- **Pandas**
- **Numpy**
- **Matplotlib**
- **Seaborn**
- **Scikit-learn**
- **Surprise**

---

## 📂 Dataset

The **Book-Crossing** dataset includes three files:

- **Users**: Contains user information like `User-ID`, `Location`, and `Age`. Some fields may have NULL values if data is unavailable.
  
- **Books**: Each book is identified by an `ISBN`, with additional details such as `Book-Title`, `Book-Author`, `Year-Of-Publication`, and `Publisher`. Only the first author is listed, and cover images are provided in three sizes: small, medium, and large, linked to Amazon.

- **Ratings**: Contains book rating data (`Book-Rating`), either as explicit ratings (1-10) or implicit ratings (0).

---

## 📋 Project Description

1. **EDA** - Performed exploratory data analysis on numerical and categorical data.
2. **Data Cleaning** - Handled missing values and outliers.
3. **Feature Selection** - Used `User-ID`, `ISBN`, and `Book-Rating` for model development.
4. **Model Development** - Implemented both popularity-based and collaborative filtering models (memory-based and model-based).

---

## ⚙️ Needs of this Project

- Data exploration
- Data processing/cleaning
- Recommendation system development

---

## 🚀 Getting Started

1. **Clone this repo**:
```bash
git clone https://github.com/your-username/Book-Recommendation-System-Project.git
```

2. **Dataset Files**:
   - **Users_data**: Available within the repository.
   - **Ratings_data**: Available within the repository.
   - **Books_data**: Available within the repository.

3. **Notebook**:
   - The complete notebook covering **Data Exploration**, **Processing**, **Transformation**, and **Model Development** is available in the repo.

---

### 📂 Repository Structure

- **Users_data.csv** - User demographics
- **Ratings_data.csv** - Ratings provided by users
- **Books_data.csv** - Details of books

---

### 🛤️ Future Enhancements

1. Integrate additional recommendation algorithms.
2. Implement a web interface for interactive recommendations.


### Happy Reading! 📖✨
