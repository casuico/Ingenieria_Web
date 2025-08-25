# adopcionesapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Comentario, Publicacion



class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email



# Login
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label or field.name
            })



class PublicacionForm(forms.ModelForm):
    vacunas = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Separar vacunas con comas'
        })
    )

    class Meta:
        model = Publicacion
        fields = [
            'nombre', 'tipo_animal', 'raza', 'edad', 'sexo',
            'castrado', 'enfermedades', 'vacunas',
            'compatibilidad_otros_animales', 'compatibilidad_ninos', 'comportamiento',
            'hogar_actual', 'condiciones_adopcion',
            'historia', 'recomendaciones_cuidado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_animal': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'castrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'enfermedades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vacunas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Separar vacunas con comas'}),
            'compatibilidad_otros_animales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'compatibilidad_ninos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comportamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hogar_actual': forms.TextInput(attrs={'class': 'form-control'}),
            'condiciones_adopcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'historia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recomendaciones_cuidado': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vacunas'].widget.attrs.update({
            'placeholder': 'Separar vacunas con comas',
            'class': 'form-control'
        })

    def clean_vacunas(self):
        vacunas_texto = self.cleaned_data.get('vacunas', '')
        if vacunas_texto:
            vacunas_lista = [v.strip() for v in vacunas_texto.split(',') if v.strip()]
            if not vacunas_lista:
                raise forms.ValidationError("El formato de las vacunas es incorrecto. Separar por comas.")
            return vacunas_lista
        return []
    
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad >=50:
            raise forms.ValidationError("La edad deber ser menor a 50 años")
        return edad
    
class MultimediaForm(forms.Form):
    archivo1 = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    archivo2 = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    archivo3 = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        archivos = [cleaned_data.get('archivo1'), cleaned_data.get('archivo2'), cleaned_data.get('archivo3')]
        archivos = [a for a in archivos if a]

        if not archivos:
            raise forms.ValidationError("Debes subir al menos un archivo.")

        for archivo in archivos:
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Cada archivo debe pesar menos de 10MB.")

        cleaned_data['archivos'] = archivos
        return cleaned_data

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe tu comentario aquí..."
            })
        }
        labels = {
            "texto": ""
        }