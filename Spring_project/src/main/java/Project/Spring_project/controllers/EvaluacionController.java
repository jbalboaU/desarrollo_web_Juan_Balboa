package Project.Spring_project.controllers;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import Project.Spring_project.models.*;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

import java.time.LocalDateTime;
import java.util.List;
import java.util.OptionalDouble;

@Controller
public class EvaluacionController {
    private final RepositorioActividad actividadRepositorio;
    private final RepositorioNota notaRepositorio;

    public EvaluacionController(RepositorioActividad actividadRepositorio, RepositorioNota notaRepositorio){
        this.actividadRepositorio=actividadRepositorio;
        this.notaRepositorio=notaRepositorio;
    }

    @GetMapping("/evaluar")
    public String listarActividadesFinalizadas(Model model){
        List<Actividad> actividades=actividadRepositorio.findActividadesFinalizadas(LocalDateTime.now());
        
        for(Actividad act : actividades){
            act.getTemas().size();
        }
        
        model.addAttribute("actividades", actividades);
        return "evaluar";
    }

    @PostMapping("/evaluar")
    @ResponseBody
    public ResponseEntity<String> agregarNota(
        @RequestParam Long actividadId,
        @RequestParam int valor
    ){
        if(valor<1 || valor>7){
            return ResponseEntity.badRequest().body("Nota inválida");
        }

        Actividad actividad=actividadRepositorio.findById(actividadId).orElse(null);
        if(actividad==null){
            return ResponseEntity.notFound().build();
        }

        Nota nota = new Nota(valor);
        nota.setActividad(actividad);
        notaRepositorio.save(nota);

        List<Nota> notas = notaRepositorio.findByActividad(actividad);
        OptionalDouble promedio = notas.stream().mapToInt(Nota::getValor).average();

        return ResponseEntity.ok(
            promedio.isPresent()
            ? String.format("%.1f", promedio.getAsDouble())
            :"-"
        );
    }
    
}
