#the libraries used
library(lme4)
library(arm)
library(pbkrtest)
#the function
anova_merMod<-function(model,rand,w=NULL,seed=round(runif(1,0,100),0),nsim=50){
  data<-model@frame
  if(!is.null(w)){
    data<-data[,-grep("(weights)",names(data))]
  }
  
  resp<-names(model.frame(model))[1]
  #generate a list of reduced model formula
  fs<-list()
  fs[[1]]<-as.formula(paste(resp,"~ 1 +",rand))
  nb_terms<-length(attr(terms(model),"term.labels"))
  if(nb_terms>1){
    for(i in 1:nb_terms){
      tmp<-c(attr(terms(model),"term.labels")[1:i],rand)
      fs[[i+1]]<-reformulate(tmp,response=resp)
    }      
  }
  
  #fit the reduced model to the data
  
  fam<-family(model)[1]$family
  if(fam=="gaussian"){
    m_fit<-lapply(fs,function(x) lmer(x,data,REML=FALSE))
  } else if(fam=="binomial"){
    m_fit<-lapply(fs,function(x) glmer(x,data,family=fam,weights=w))
  }  else{
    m_fit<-lapply(fs,function(x) glmer(x,data,family=fam))
  }
  
  #compare nested model with one another and get LRT values (ie increase in the likelihood of the models as parameters are added)
  tab_out<-NULL
  
  for(i in 1:(length(m_fit)-1)){
    comp<-PBmodcomp(m_fit[[i+1]],m_fit[[i]],seed=seed,nsim=nsim)    
    term_added<-attr(terms(m_fit[[i+1]]),"term.labels")[length(attr(terms(m_fit[[i+1]]),"term.labels"))]
    #here are reported the bootstrapped p-values, ie not assuming any parametric distribution like chi-square to the LRT values generated under the null model
    #these p-values represent the number of time the simulated LRT value (under null model) are larger than the observe one
    tmp<-data.frame(term=term_added,LRT=comp$test$stat[1],p_value=comp$test$p.value[2])
    tab_out<-rbind(tab_out,tmp)
    print(paste("Variable ",term_added," tested",sep=""))
  }  
  print(paste("Seed set to:",seed))
  return(tab_out)  
}