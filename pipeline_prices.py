import logging
logging.basicConfig(level=logging.INFO)
import subprocess
import datetime

logger = logging.getLogger(__name__)

retail_sites_uids = ['alkosto', '']
categories_sites_uids = ['telefonos', 'computadores-tablets','televisores','electrodomesticos','audio','video-juegos','accesorios','camaras','netflix-otros','smartwatch','deportes','hogar-muebles']
pages = [7,6,4,41,12,5,18,1,2,2,5,8]

def main(date):
    _extract(date)
    _transform(date)
    _load(date)

def _extract(date):
    logger.info('Starting extract process')
    for i in range(len(categories_sites_uids)):
        subprocess.run(['python3', 'prices_scraper.py', retail_sites_uids[0], categories_sites_uids[i], str(pages[i])], cwd='./prices_scraper')
        
        logger.info('Making HTML backup folder..................')
        subprocess.run(['mkdir', date], cwd='./prices_scraper/fuente/'+categories_sites_uids[i])
        subprocess.run(['find', '.', '-name', '*'+date+'.html', 
                '-exec', 'mv', '{}', './'+date, ';'],
                cwd='./prices_scraper/fuente/'+categories_sites_uids[i])
        
    logger.info('Moving files to raw.................')
    subprocess.run(['mkdir', date], cwd='./prices_scraper/raw')
    subprocess.run(['find', '.', '-name', '*'+date+'.csv', 
                '-exec', 'mv', '{}', './raw/'+date, ';'],
                cwd='./prices_scraper')

def _transform(date):
    logger.info('Starting cleaning all files of {}'.format(date))

    logger.info('Copying files from raw.................')
    subprocess.run(['find', '.', '-name', '*.csv', 
                '-exec', 'cp', '{}', '../../../prices_cleaner', ';'],
                cwd='./prices_scraper/raw/'+date)

    logger.info('Cleaning all files....................')
    for i in range(len(categories_sites_uids)):
        subprocess.run(['find', '.', '-name', '{}*'.format(categories_sites_uids[i]), 
                    '-exec', 'python3', 'prices_cleaner.py', '{}', date, ';'],
                    cwd='./prices_cleaner')

    logger.info('Moving cleaned files..................')
    subprocess.run(['find', '.', '-name', 'clean_*', 
                '-exec', 'mv', '{}', '../prices_load', ';'],
                cwd='./prices_cleaner')

    logger.info('Deleting raw files..................')
    subprocess.run(['find', '.', '-name', '*csv', 
                '-exec', 'rm', '{}', ';'],
                cwd='./prices_cleaner')
    
def _load(date):
    logger.info('Load {} data to db....................'.format(date))
    for i in range(len(categories_sites_uids)):
        subprocess.run(['find', '.', '-name', 'clean_{}*'.format(categories_sites_uids[i]), 
                    '-exec', 'python3', 'prices_load.py', categories_sites_uids[i]+'_db.csv' , '{}' , categories_sites_uids[i] , date, ';'],
                    cwd='./prices_load')

    logger.info('Copying db files for backup.................')
    subprocess.run(['find', '.', '-name', '*_db.csv', 
                '-exec', 'cp', '{}', '../prices_db', ';'],
                cwd='./prices_load')

    logger.info('Deleting clean files..................')
    subprocess.run(['find', '.', '-name', 'clean_*', 
                '-exec', 'rm', '{}', ';'],
                cwd='./prices_load')

    logger.info('Making backup folder..................')
    subprocess.run(['mkdir', date], cwd='./backup')
    subprocess.run(['find', '.', '-name', '*_db.csv', 
                '-exec', 'cp', '{}', '../backup/'+date, ';'],
                cwd='./prices_load')

if __name__ == '__main__':
    now = datetime.datetime.now()
    main(now.strftime('%d_%m_')+now.strftime("%y"))