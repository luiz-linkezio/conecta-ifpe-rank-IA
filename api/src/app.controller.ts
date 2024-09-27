import { Controller, Post, UploadedFile, UseInterceptors, Res } from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { Response } from 'express';
import { exec } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

@Controller('rank-ia')
export class AppController {
  @Post('process-xlsx')
  @UseInterceptors(FileInterceptor('file'))
  async processXlsx(
    @UploadedFile() file: Express.Multer.File,
    @Res() res: Response
  ) {
    const uploadsDir = path.join(__dirname, '..', 'uploads');
    const filePath = path.join(uploadsDir, 'input.xlsx');

    // Cria o diretório 'uploads' se não existir
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir);
    }

    // Salva o arquivo no diretório 'uploads'
    fs.writeFileSync(filePath, file.buffer);

    // Especifique o caminho completo do executável Python
    const pythonPath = path.join(__dirname, '..', '..', 'rank-ia', 'virtualenv', 'Scripts', 'python.exe');
    const scriptPath = path.join(__dirname, '..', '..', 'rank-ia', 'src', 'main.py');

    // Executa o script Python passando o caminho do arquivo
    exec(`"${pythonPath}" "${scriptPath}" "${filePath}"`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Erro ao executar o script Python: ${error.message}`);
        return res.status(500).json({ error: 'Erro ao processar o arquivo' });
      }

      // Verifica se o arquivo processado existe
      const processedFilePath = path.join(uploadsDir, 'processed_output.xlsx');
      if (fs.existsSync(processedFilePath)) {
        // Retorna o arquivo processado para o cliente
        res.download(processedFilePath, (err) => {
          if (err) {
            console.error('Erro ao enviar o arquivo:', err);
          }
          // Exclui o arquivo após o envio
          fs.unlinkSync(filePath);
          fs.unlinkSync(processedFilePath);
        });
      } else {
        res.status(500).json({ error: 'Erro ao encontrar o arquivo processado' });
      }
    });
  }
}
