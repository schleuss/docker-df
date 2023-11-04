# Docker - disk usage

Script utility to verify docker volume usage

## Run 

### Directly with docker

```bash
docker run -it --rm \
    -v "/var/run/docker.sock:/var/run/docker.sock" \
    -v "/var/lib/docker:/var/lib/docker" schleuss/docker-df:latest
```

### With utility shell script 

```bash
./docker-df.sh
```

## Ouput 

Run  the default option, to list all containers 

```bash
$ ./docker-df.sh 
=================================================================================================================================================
  Id            Nome                                                                                          Tamanho           Tamanho (Bytes)
=================================================================================================================================================
  4f79034bfab7  mongodb                                                                                      836.6MiB                 877201152
  9ce01a287f2b  pgsql                                                                                        704.4MiB                 738613084
  145196d7886c  env_prometheus_1                                                                                34.0B                        34
  a339fdb16288  env_alertmanager_1                                                                               0.0B                         0
-------------------------------------------------------------------------------------------------------------------------------------------------
```
Get the full details of a container

```bash
$ ./docker-df.sh  9ce01a287f2b
======================================================================================================================================================
 Nome: pgsql
 Id  : 9ce01a287f2be178b1f03d28d057608155a43b6d77d03605b00f060b96488071
======================================================================================================================================================
          Tamanho           Tamanho (Bytes) Path                                                                                                
======================================================================================================================================================
         352.2MiB                 369306542 /var/lib/docker/overlay2/1bda419514a2daf1c98cd23ac136f428aff65a67376c19785130a0c8587acd6b/merged    
         352.2MiB                 369306542 /var/lib/docker/overlay2/1bda419514a2daf1c98cd23ac136f428aff65a67376c19785130a0c8587acd6b/diff      
             0.0B                         0 /var/lib/docker/overlay2/1bda419514a2daf1c98cd23ac136f428aff65a67376c19785130a0c8587acd6b/work      
             0.0B                         0 /var/lib/docker/volumes/efb37d8244429e89b99f34a997244d3d2b770e38b975ab3925519edcdc7ac6e8/_data      
--------------------------------------------------
         704.4MiB                 738613084 Total              
```         

