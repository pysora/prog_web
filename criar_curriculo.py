import bd

mysql = bd.SQL("root", "", "test")

comando = "DROP TABLE IF EXISTS curriculo;"

if mysql.executar(comando, ()):
   print ("Tabela de currículos excluída com sucesso!")


comando = '''
CREATE TABLE curriculo (
         idt_curriculo INT AUTO_INCREMENT PRIMARY KEY, 
         nome VARCHAR(50) NOT NULL, 
         dta_nasc DATE NOT NULL,
         ling_prog TEXT NOT NULL, 
         inst_ensino VARCHAR(20),  
         curso VARCHAR(30),
         semestre INT,
         celular VARCHAR(30) NOT NULL,
         email VARCHAR(50) NOT NULL);
'''
comando2 = '''
INSERT INTO curriculo(nome, ling_prog, inst_ensino, curso, semestre, celular, email) VALUES('Henrique Tolentino Costa Ribeiro', 'JavaScript, Python e SQL', 'Ceub', 'Ciência da Computação', 5, '(61) 98108-0055', 'henriquetcr@gmail.com');
'''

if mysql.executar(comando, ()):
   print ("Tabela de currículos criada com sucesso!")

if mysql.executar(comando2, ()):
   print ("Dados do currículo adicionados com sucesso!")

