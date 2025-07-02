CREATE TABLE IF NOT EXISTS `tarea2`.`nota` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `actividad_id` INT NOT NULL,
  `valor` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_nota_actividad1_idx` (`actividad_id` ASC),
  CONSTRAINT `fk_nota_actividad1`
    FOREIGN KEY (`actividad_id`)
    REFERENCES `tarea2`.`actividad` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

ALTER TABLE nota DROP COLUMN nota;

