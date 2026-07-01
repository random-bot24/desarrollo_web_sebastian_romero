package tarea4.tarea_sr.controllers;

public class ActividadDTO {
    private Integer id;
    private String nombreMiembro;
    private String dia;
    private String tipo;
    private String comuna;
    private String nombreActividad;
    private String descripcion;
    private String nota; // Es String para poder enviar el "-" si no hay nota

    // Genera el constructor vacío, un constructor con todos los campos, y los Getters/Setters correspondientes.
    
    public ActividadDTO(Integer id, String nombreMiembro, String dia, String tipo, String comuna, String nombreActividad, String descripcion, String nota) {
        this.id = id;
        this.nombreMiembro = nombreMiembro;
        this.dia = dia;
        this.tipo = tipo;
        this.comuna = comuna;
        this.nombreActividad = nombreActividad;
        this.descripcion = descripcion;
        this.nota = nota;
    }

    public Integer getId() { return id; }
    public String getNombreMiembro() { return nombreMiembro; }
    public String getDia() { return dia; }
    public String getTipo() { return tipo; }
    public String getComuna() { return comuna; }
    public String getNombreActividad() { return nombreActividad; }
    public String getDescripcion() { return descripcion; }
    public String getNota() { return nota; }

}
