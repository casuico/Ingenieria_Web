"""
Formularios personalizados para la aplicación adopcionesapp.
Incluye formularios de registro, autenticación, publicaciones, animales, multimedia y comentarios.
"""

# adopcionesapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Animal, Comentario, Publicacion

class RegistroForm(UserCreationForm):
    """
    Formulario de registro de usuario extendido con validación de email único.
    """
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

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de autenticación personalizado para mejorar la experiencia de usuario.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label or field.name
            })

class AnimalForm(forms.ModelForm):
    """
    Formulario para la creación y edición de animales.
    """
    class Meta:
        model = Animal
        fields = [
            'nombre', 'tipo_animal', 'raza', 'edad', 'sexo',
            'castrado', 'enfermedades', 'vacunas',
            'compatibilidad_otros_animales', 'compatibilidad_ninos', 'comportamiento'
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
            'comportamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad >= 250:
            raise forms.ValidationError("La edad debe ser menor a 250 años")
        return edad

class PublicacionForm(forms.ModelForm):
    """
    Formulario para la creación de publicaciones de adopción.
    """
    class Meta:
        model = Publicacion
        fields = [
            'titulo',
            'condiciones_adopcion',
            'historia',
            'recomendaciones_cuidado',
            'hogar_actual'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'condiciones_adopcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'historia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recomendaciones_cuidado': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hogar_actual': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PublicacionEditarForm(forms.ModelForm):
    """
    Formulario para la edición de publicaciones de adopción.
    """
    class Meta:
        model = Publicacion
        fields = [
            'titulo',
            'condiciones_adopcion',
            'historia',
            'recomendaciones_cuidado',
            'hogar_actual',
            'adoptado'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'condiciones_adopcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'historia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recomendaciones_cuidado': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hogar_actual': forms.TextInput(attrs={'class': 'form-control'}),
            'adoptado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MultimediaForm(forms.Form):
    """
    Formulario para la carga de archivos multimedia (imágenes y videos) asociados a una publicación.
    """
    archivo1 = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    archivo2 = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))
    archivo3 = forms.FileField(required=False, widget=forms.FileInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.publicacion = kwargs.pop('publicacion', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        archivos = [cleaned_data.get('archivo1'), cleaned_data.get('archivo2'), cleaned_data.get('archivo3')]
        archivos = [a for a in archivos if a]

        if not archivos and (not self.publicacion or not self.publicacion.multimedia.exists()):
            raise forms.ValidationError("Debes subir al menos un archivo.")

        for archivo in archivos:
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Cada archivo debe pesar menos de 10MB.")

        cleaned_data['archivos'] = archivos
        return cleaned_data

class ComentarioForm(forms.ModelForm):
    """
    Formulario para la creación de comentarios en publicaciones.
    """
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