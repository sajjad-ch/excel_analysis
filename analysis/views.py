from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import UserFiles
from .forms import FileForm, PlotForm
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import pandas as pd
import io, os
import base64
import matplotlib
import openai
from dotenv import load_dotenv
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from transformers import pipeline
import ollama

@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        user_files = UserFiles.objects.filter(user=request.user)
        context = {
            'user_files': user_files,
            'user': request.user.first_name
        }
        return render(request, 'analysis/home.html', context)


@method_decorator(login_required, name='dispatch')
class UploadFileView(View):
    def get(self, request):
        fileform = FileForm()
        context = {
            'fileform': fileform
        }
        return render(request, 'analysis/uploadfile.html', context)

    def post(self, request: HttpRequest):
        fileform = FileForm(request.POST, request.FILES)
        user = request.user
        if fileform.is_valid():
            user_file = fileform.save(commit=False)
            user_file.file_name = str(fileform.cleaned_data['file'])
            user_file.user = user
            user_file.save()
            return redirect(reverse('DataSummary', kwargs={'file': str(fileform.cleaned_data['file'])}))
        context = {
            'fileform': fileform
        }
        return render(request, 'analysis/uploadfile.html', context)


@method_decorator(login_required, name='dispatch')
class DataSummaryView(View):
    def get(self, request: HttpRequest, file):
        user = request.user
        user_file = UserFiles.objects.filter(user=user, file_name=file).only('file').first()
        if not user_file:
            return redirect('UploadFile')
        file_path = user_file.file.path
        extension = str(user_file).split('.')[-1].lower()
        try:
            if extension == 'csv':
                df = pd.read_csv(file_path)
            elif extension == 'xlsx':
                df = pd.read_excel(file_path)
            elif extension == 'xls':
                df = pd.read_excel(file_path, engine='xlrd')
            elif extension == 'db' or extension == 'sqlite':
                df = pd.read_sql(file_path)
            else:
                return redirect('UploadFile')
        except Exception as e:
            # Handle any errors that occur during file reading
            print(f"Error reading file: {e}")
            return redirect('UploadFile')
        df = DataCleaning(df=df)
        ds = df.head()
        rows = ds.to_dict(orient='records')
        columns = df.columns.tolist()
        description = df.describe().reset_index()
        desc_rows = description.to_dict(orient='records')
        desc_columns = description.columns.tolist()

        context = {
            'user_file_name': user_file.file_name,
            'columns': columns,
            'rows': rows,
            'desc_columns': desc_columns,
            'desc_rows': desc_rows,        
        }
        return render(request, 'analysis/data-summary.html', context)


def DataCleaning(df):
    # Drop empty cells
    df.dropna(inplace=True)
    # Drop Duplicates rows 
    df.drop_duplicates(inplace = True)
    
    return df

    
@method_decorator(login_required, name='dispatch')
class PlotingView(View):
    def get(self, request):
        plotform = PlotForm()
        context = {
            'plotform': plotform
        }
        return render(request, 'analysis/plot.html', context)

    def post(self, request):
        plotform = PlotForm(request.POST)
        if plotform.is_valid():
            plot_type = plotform.cleaned_data['kind']
            x_axis = plotform.cleaned_data['x_axis']
            y_axis = plotform.cleaned_data['y_axis']
            user = request.user
            user_file = UserFiles.objects.filter(user=user).only('file').first()
            if not user_file:
                return redirect('UploadFile')
            file_path = user_file.file.path
            extension = str(user_file).split('.')[-1].lower()
            try:
                if extension == 'csv':
                    df = pd.read_csv(file_path)
                elif extension == 'xlsx':
                    df = pd.read_excel(file_path, engine='openpyxl')
                # elif extension == 'xls':
                #     df = pd.read_excel(file_path, engine='xlrd')
                else:
                    return redirect('UploadFile')
            except Exception as e:
                print(f"Error reading file: {e}")

            if plot_type and x_axis in df.columns and y_axis in df.columns:
                # Generate plot
                fig, ax = plt.subplots()
                df.plot(kind=str(plot_type), x=str(x_axis), y=str(y_axis), ax=ax)
                ax.set_title(f"{plot_type.capitalize()} Plot of {x_axis} vs {y_axis}")

                # Save plot to a BytesIO object
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)
                plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
                buf.close()
                return render(request, 'analysis/plot.html', context={'plot_data': plot_data, 'plotform': plotform})
        return render(request, 'analysis/plot.html', {'plotform': plotform})



class AiReportView(View):
    def get(self, request, file):
        # Get the file object
        user = request.user
        user_file = UserFiles.objects.filter(user=user, file_name=file).only('file').first()
        
        # Read the file
        file_path = user_file.file.path
        try:
            extension = file_path.split('.')[-1].lower()
            # test1.csv  ==> ['test1', 'csv']
            if extension == 'csv':
                df = pd.read_csv(file_path)
            elif extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                return redirect('UploadFile')  # Handle unsupported file types
        except Exception as e:
            print(f"Error reading file: {e}")
            return redirect('UploadFile')

        # Process the file with AI (example API call or model integration)
        # Assuming we have a function `get_ai_advice` that takes a DataFrame and returns advice
        summary = {
            "columns": df.columns.tolist(),
            "shape": df.shape,
            # "missing_valuse": df.isnull().sum().to_dict(),
            "basic_stats": df.describe().to_dict()
        }
        try:
            ai_advice = get_ai_advice(summary)  # Replace this with your AI interaction logic
            # ai_advice = explain_summary(summary)
        except Exception as e:
            print(f"Error processing file with AI: {e}")
            ai_advice = ["Error processing file. Please try again later."]

        # Render the advice in the template
        context = {
            'file_name': file,
            'advice': ai_advice,
        }
        return render(request, 'analysis/ai_report.html', context)


# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_ai_advice(df_markdown):
#     prompt = f"""
#     Analyze the following table and provide actionable insights for improvement:
#     {df_markdown}
#     """
#     response = openai.ChatCompletion.create(  # Updated to ChatCompletions
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an expert data analyst."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=500,
#         temperature=0.7,
#     )
#     return response.choices[0].message.content.splitlines()


def get_ai_advice(summary):
    prompt = f"""
    I have a data file with the following information:
    Columns: {summary["columns"]}
    Shape (rows, columns): {summary["shape"]}
    Basic statistics: {summary["basic_stats"]}

    Please explain what this data shows, identify any patterns or outliers, and provide suggestions or observations like a professional data analyst.
    """
    
    try:
        response = ollama.chat(
            model='mistral',  # Make sure you pulled this with `ollama pull mistral`
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content'].splitlines()
    except Exception as e:
        print("Error calling Ollama:", e)
        return ["Error communicating with local AI model."]



class DecisionView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


class FilesView(View):
    def get(self, request):
        user_files = UserFiles.objects.filter(user=request.user)
        context = {
            'user_files': user_files,
            'user': request.user.first_name
        }
        return render(request, 'analysis/files.html', context)