import {useEffect,useState} from 'react';
export function useJourney(){
  const [study,setStudy]=useState(()=>{try{const value=JSON.parse(localStorage.getItem('pattern-atlas-journey-v1'));return {blocks:Array.isArray(value?.blocks)?value.blocks:[],readiness:Array.isArray(value?.readiness)?value.readiness:[],challenges:Array.isArray(value?.challenges)?value.challenges.filter(x=>typeof x==='string'):[]};}catch{return {blocks:[],readiness:[],challenges:[]};}});
  const [storage,setStorage]=useState(true);
  useEffect(()=>{try{localStorage.setItem('pattern-atlas-journey-v1',JSON.stringify(study));setStorage(true);}catch{setStorage(false);}},[study]);
  return {study,setStudy,storage};
}
