import { Controller, Post, UploadedFile, UseInterceptors, Res } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';
import * as XLSX from 'xlsx';
import { exec } from 'child_process'; // Adicione esta linha para importar 'exec'

@Controller('rank-ia')
export class AppController {
  @Post('classificar-alunos')
  @UseInterceptors(FileInterceptor('file'))
  async processXlsx(
    @UploadedFile() file: Express.Multer.File,
    @Res() res: Response
  ) {
    const uploadsDir = path.join(__dirname, '..', 'uploads');

    const inputPath = path.join(uploadsDir, 'input.xlsx');
    const outputPath = path.join(uploadsDir, 'processed_output.xlsx');

    // Cria o diretório 'uploads' se não existir
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir);
    }

    // Salva o arquivo no diretório 'uploads'
    fs.writeFileSync(inputPath, file.buffer);

    // Especifique o caminho completo do executável Python
    const pythonPath = path.join(__dirname, '..', '..', 'rank-ia', 'venv', 'Scripts', 'python.exe');
    const scriptPath = path.join(__dirname, '..', '..', 'rank-ia', 'src', 'main.py');

    // Executa o script Python passando o caminho do arquivo
    exec(`"${pythonPath}" "${scriptPath}" "${inputPath}" "${outputPath}"`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Erro ao executar o script Python: ${error.message}`);
        return res.status(500).json({ error: 'Erro ao processar o arquivo' });
      }

      // Verifica se o arquivo processado existe
      const processedFilePath = path.join(uploadsDir, 'processed_output.xlsx');
      if (fs.existsSync(processedFilePath)) {
        // Lê o arquivo Excel processado e converte para JSON
        const workbook = XLSX.readFile(processedFilePath);
        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];

        // Converte a planilha para JSON
        const jsonData = XLSX.utils.sheet_to_json(sheet);

        // Retorna o JSON como resposta
        res.json({ data: jsonData });

        // Exclui os arquivos após o processamento
        fs.unlinkSync(inputPath);
        fs.unlinkSync(processedFilePath);
      } else {
        res.status(500).json({ error: 'Erro ao encontrar o arquivo processado' });
      }
    });
  }
}
