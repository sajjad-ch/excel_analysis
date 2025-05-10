
---

```markdown
# sajjad-ch-excel_analysis

A Django-based web application for analyzing Excel files with user authentication and AI-assisted reporting. This project supports user registration, file uploads, and interactive data visualization.

---

## 📁 Project Structure


---

## 🚀 Features

- ✅ User registration and login
- 🔐 Password reset functionality
- 📁 Excel file upload
- 📊 Data summaries and visualizations
- 🧠 AI-generated reports
- 📂 Admin interface with custom styles

---

## 🛠 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/sajjad-ch-excel_analysis.git
   cd sajjad-ch-excel_analysis
````

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the server**:

   ```bash
   python manage.py runserver
   ```

---

## 👤 User Authentication

* Register a new account at `/register/`
* Login at `/login/`
* Reset password through `/forgot-password/`

---

## 📈 Excel Analysis Workflow

1. Upload your Excel file via the **Upload File** page.
2. The app processes the data and generates:

   * Summarized tables
   * Interactive plots
   * AI-powered analysis reports

---

## 🖼 UI Templates

* `account/`:

  * `register.html`
  * `login.html`
  * `forgot_password.html`
  * `reset_password.html`

* `analysis/`:

  * `uploadfile.html`
  * `data-summary.html`
  * `plot.html`
  * `ai_report.html`



## 📦 Static Files

Custom static files for admin interface and UI enhancements:

* CSS stylesheets
* JavaScript functionality (filters, widgets, datepickers)
* Images and vendor libraries (jQuery, Select2)



## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.



## 🙋‍♂️ Author

**Sajjad Ch**
Feel free to reach out for collaboration or feedback!


